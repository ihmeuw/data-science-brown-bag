This document covers:

* What are array jobs
* Why to use array jobs
* How to use array jobs
* Challenges


# What is an array job?

An array job is an concise way to submit a set of jobs to the cluster. A
common task at the IHME is to run a script N times for a set of arguments. One
approach is to loop through the set of arguments and submit a qsub for each
argument. Another approach (the array job approach) is to submit a single qsub
as an array job, and have the script figure out what its arguments are. In
pseudo-code, the two approaches are provided below:

First approach:
```
func script(argument)
    do something with argument

func submit_qsub():
    for argument in arguments:
        qsub(script, argument)
```

Array job alternative approach:
```
func script():
    task_id = get_sge_task_id()
    argument = arguments[task_id]
    do something with argument

func submit_qsub():
    N = len(arguments)
    qsub_array_job(script, N)
```

The main difference for the user is that instead of looping through your
arguments to figure out what the argument to your script is, the script figures
out (with the help of sge and sge\_task\_id) what its argument is.

## Syntax
To submit a qsub from the command line, there are two options. The first is
**`qsub -t START:STOP`** and the other is **`qsub -t START-STOP:STEP`**. I find
that steps are not useful, and that starting at ``1`` is most practical, so I
am always using **`qsub -t 1:N`**, where ``N`` is the number of jobs you want
to execute.

One thing to note is that `START` must be greater than 0.


# Why Array Jobs?

tl,dr: Array jobs lighten the load to our wonderful SGE scheduler.

Suppose there was a job that needed to be run in parallel for each cause,
location 2-tuple. For simplicity, suppose there were 150 causes and 200
locations. Then 30,000 jobs would have to be submitted. Traditionally, each job
is submitted as an individual job, which means the scheduler node has to keep
track of 30,000 distinct set of job requirements (even though they are
identical). If submitted as an array job, the scheduler would know to only keep
one job requirement, and use that 30,000 times while submitting all of the
jobs. One is a lot less than 30,000 - imagine holding one grape versus 30,000
grapes. You wouldn't want to burden the scheduler with 30,000 grapes!

## From Falko:
When the scheduler node is over burdened (because people aren't using array
jobs), it becomes very expensive to submit a qsub. With array jobs, we only
need to submit a single qsub. With array jobs, we'd have to submit 30,000
qsubs. If each qsub took half a second, then that would lead to four hours of
qsubbing, which is a huge cost.

## Extra benefits:
With ``qstat``, using array jobs makes the output more readable. Array jobs
also help simplify holds on jobs, which I'll get to later.


# How to use array jobs

These examples will all be done in bash. All the examples are summarized in
`bash_examples.sh`.

There are coding examples showing how to do use array jobs
in Python, but that's in the appendix.

## Simple Example
The use-case here is printing the numbers 1 through 10 with a qsub.

### Not an array job:

``for i in `seq 1 10`; do qsub -b y echo $i; done;``

The output shows ten separate jobs being submitted:
```
Your job 13398651 ("echo") has been submitted
Your job 13398652 ("echo") has been submitted
Your job 13398653 ("echo") has been submitted
Your job 13398654 ("echo") has been submitted
Your job 13398655 ("echo") has been submitted
Your job 13398656 ("echo") has been submitted
Your job 13398657 ("echo") has been submitted
Your job 13398658 ("echo") has been submitted
Your job 13398659 ("echo") has been submitted
Your job 13398660 ("echo") has been submitted
```

### An array job:

`qsub -b y -t 1:10 'echo $SGE_TASK_ID'`

This will be a single array job, with one task id with 10 jobs associated with
it: **`Your job-array 13398664.1-10:1 ("echo $SGE_TASK_ID") has been
submitted`**

## Holding on array jobs

There are two ways to hold a job on an array job. You can wait for the entire
array to finish, or you can wait on specific jobs within the array to finish.
For the examples below, suppose the following array job was running with job id
6:

**`qsub -b y -t 1:10 sleep 1000`**

If you wanted to run another job after the sleep array finished you could do so
with **`-hold_jid 6`**. It doesn't matter if the next job is a single qsub, or
another array job. For example, **`qsub -b y -hold_jid 6 echo hello world`**.

If you want to wait on specific jobs within the array to finish, there are some
caveats. It only works array jobs and only if the next array job's **`START`**
and **`STOP`** match the original job. This means you cannot hold a single qsub
on one job from an array job, and you cannot hold an array job that doesn't map
into perfectly onto the original array job's task array. Practically, the only
way to use this is if you're doing an array over the same exact things: **`qsub
-b y -t 1:10 -hold_jid_ad 6 'echo $SGE_TASK_ID''`**.


# Challenges

## Changing your scripts

To use array jobs, the scripts have to be restructured so that they use the
**`SGE_TASK_ID`** environment variable to define its arguments. This can be
annoying because you lose the ability to quickly run the script through the
command line. One solution can be to provide argument passing through either
SGE TASK ID or command line arguments. Some pseudo-code below:

```
func main():
    if "SGE_TASK_ID" is available:
        arguments = list_of_arguments[task_id]
    else:
        arguments = get_arguments_from_command_line()
```

## Off-by-one bugs

You cannot start array jobs at 0. This is annoying for Python because indices
start at 0 in Python. You'll need to be careful when adding and subtracting one
to get the correct displacement for whatever language you work in.

## Environment variables

There's a lot going on with environment variables. **`SGE_TASK_ID`** is just
one of many environment variables, and it is created by SGE when you submit
array jobs. As a user, the minimum knowledge you need to know about environment
variables is how to read them (e.g. **`os.environ.get`**). I would recommend
learning more about environment variables (like in your **`.bashrc`**), because
they are useful!

## Restricted to one dimension

Array jobs are by nature one dimensional, but usually we loop over lots of
different dimensions (e.g. all locations, sexes, years, and causes). To be able
to use array jobs over higher dimensions, you will need to enumerate your
N-tuples. The actual order of the N-tuples can be arbitrary, but as long as it
is consistent.


# APPENDIX

This section will cover the Python code in this folder and how it relates to
array jobs.

The qsub submitter functions are in **`qsubber.py`**. There are three
functions, corresponding to three scripts.

1. **`submit_normal_jobs`** will loop over locations and years and submit a
   separate qsub for each one. The script it calls is **`run.py`** , which is
made to parse command line arguments.

2. **`submit_array_jobs`** will submit a single array job qsub. The script it
   calls is **`run_array.py`**, which is made to use SGE TASK ID to figure out
what location and year its arguments are.

3. **`try_combined_script`** will submit a single qsub with command line
   arguments, and submit a single array job. The script it calls is
**`run_combined.py`**, which is made to handle both parsing arguments from the
command line and using SGE TASK ID.
