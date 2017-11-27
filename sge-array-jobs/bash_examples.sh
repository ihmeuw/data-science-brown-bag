# You probably shouldn't run this, otherwise you'll submit a bunch of random
# qsubs.

# Not array job
for i in `seq 1 10`; do qsub -b y echo $i; done;

# Array job
qsub -b y -t 1:10 'echo $SGE_TASK_ID'

# Holding on an entire array
qsub -hold_jid <array-job-id> -b y echo "hello world"
qsub -hold_jid <array-job-id> -b y -t 1:123 echo "the size of this array doesn't need to match the job it is holding on"

# Holding an array on another array
qsub -hold_jid_ad <array-job-id> -b y -t 1:10 echo "the size of this array does need to align with the job it is holding on"
qsub -hold_jid_ad <array-job-id> -b y -t 1-10:3 echo "it doesn't have to be one-to-one but START and STOP have to match"
