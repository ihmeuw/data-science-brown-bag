# Command Line Data Science Pt 1
## Why do your data science at the command line?
- Nearly universal
	- We'll focus on Bash tools that [almost] all *nix systems have
- Great support for streaming
	- Do things without having to load gigantic datasets into memory
- Easy workflows
	- Use pipes to string together commands easily
- You're already there!
	- Make reusable functions to have common needs accessible with a few keystrokes

## The basics
### Redirection
Use `>` to send your `stdout` to a file
```bash
ls -lah ~ > my-home.txt
```
or `>>` to append to an existing file
```bash
echo "thing1" > things.txt
echo "thing2" >> things.txt
```
And it works with any command that writes to `stdout`
```bash
curl http://www.gutenberg.org/files/76/76-0.txt > huckfinn.txt
```
See [I/O Redirection](https://www.tldp.org/LDP/abs/html/io-redirection.html) for more, including separating `stdout` from `stderr`
### Pipes
Use `|` to pipe your `stdout` into another command
```bash
cat my-home.txt | head -n5
```
These can be endlessly strung together and combined.
```bash
cat my-home.txt | head -n10 | tail -n5 > part-of-my-home.txt
```
See [Pipes](http://tldp.org/HOWTO/Bash-Prog-Intro-HOWTO-4.html) for more
### Aliases
Think of them like shortcuts for commonly used commands
```bash
alias running='qstat -s r' 
```
or convenient defaults
```bash
alias lls='ls -lah'
```
or even overwrite standard behavior (risky, but some people love it... _caveat emptor_)
```bash
alias ls='ls -lah'
```
See [tldr - alias](https://tldr.ostera.io/alias) for more
### Functions
For when you've graduated beyond aliases
```bash
function_name() {
	# do some stuff
}
```
probably because you want to add (_positional_) arguments
```bash
hello_you() {
	echo "Hello, $1"
} 
```
some of which can be optional if you want
```bash
hello_yall() {
    if [ -z "$2" ]
    then other="friends"
	else other="$2"
	fi
	echo "Hello, $1 and $other"
}
```
And they can get pretty complicated if you want.... see [Complex Functions and Function Complexities](http://tldp.org/LDP/abs/html/complexfunct.html)
### grep
Search for a pattern and only return those lines that match it
```bash
cat things.txt | grep 1
```
and works with regular expressions (see Falko's talk, which I'll link to here as soon as he puts it on the github)
```bash
cat huckfinn.txt | grep "Jim"
cat huckfinn.txt | grep "^Jim"
``` 
See [tldr - grep](https://tldr.ostera.io/grep) for more
### sed
A "stream editor" that allows you to do some basic text transformations
```bash
echo "hello world" | sed 's/world/friend/'
```
including on files
```bash
sed 's/Jim/James/' huckfinn.txt > huckfinn-James.txt
# or in place, if you're reckless: sed -i 's/Jim/James/' huckfinn.txt
```
There's also a [ton of sed commands](https://www.gnu.org/software/sed/manual/sed.html#sed-commands-list) that you can use.
For instance, `d` to delete lines
```bash
qstat | sed '1,2d'
```
or `a` to append them
```bash
seq 5 | sed '2a hello'
```
or string together multiple commands using `;`
```bash
seq 7 | sed 'n;n;s/./x/'
```
### awk
`awk` is a whole text processing and data extraction language created at Bell Labs in the 70s. It could be a whole course unto itself, so for today I'm just going to provide a couple examples. 
```bash
echo "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." | awk '{ print $6 }'
```

```bash
ls -lah | 
awk 'BEGIN { print "File\tOwner" }; { print $10, "\t", $3 }; END { print " - END - " }'
```
The best tutorial I've seen on `awk` is [this one](http://www.grymoire.com/Unix/Awk.html)
## Some useful examples
### job_stats
A function to find out how many of each type of job you - or someone else - has running or queued up on the cluster:
```bash
job_stats() { 
    if [ -z "$1" ]
    then U=$USER
    else U=$1
    fi
    echo `qstat -u $U | sed 1,2d | awk '{ print $5 }' | sort | uniq -c` 
}
```
### kill em all
Another way to kill all jobs that match a certain pattern (e.g. everything that isn't a qlogin)
```bash
qstat | grep -v QLOGIN | awk {'print $1'} | xargs qdel
```
You can wait to add the `xargs qdel` til the very end in order to see what you're actually going to kill
### Transpose a CSV
We'll walk through this one in detail in part II....
```bash
#!/bin/awk -f
BEGIN {FS=OFS=","} {
	for (i=1;i<=NF;i++) {
		arr[NR,i]=$i;
		if(big <= NF)
	 		big=NF;
	}
}
END {
  for(i=1;i<=big;i++) {
    	for(j=1;j<=NR;j++) {
    		printf("%s%s",arr[j,i], (j==NR ? "" : OFS));
		}
    	print "";
   }
}
```
