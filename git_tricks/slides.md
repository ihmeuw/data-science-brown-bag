% Git tricks

# Setup


```
[tmp]$ git init talk_repo
Initialized empty Git repository in /tmp/talk_repo/.git/
[tmp]$ cd talk_repo/
[talk_repo]$ ls
[talk_repo]$ echo 'print("Hello, World!")' > test_file.py
[talk_repo]$ ls
test_file.py
```

--------

# Staging Area

```
[talk_repo]$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)

        test_file.py

nothing added to commit but untracked files present (use "git add" to track)

[talk_repo]$ git add test_file.py
[talk_repo]$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   test_file.py

```

--------


```
[talk_repo]$ echo 'print("Goodbye, World :(")' > test_file.py
[talk_repo]$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   test_file.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   test_file.py

```


---------


```
[talk_repo]$ git add test_file.py 
[talk_repo]$ git status
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   test_file.py

[talk_repo]$ git commit -m"Adding test file"
[talk_repo]$ git status
On branch master
nothing to commit, working tree clean
```


-------

# Commiting Partial Changes

```
[talk_repo]$ cat > test_file.py << EOF
print('New First Line')
print('Goodbye, World :(')
print('New Last Line')
EOF
[talk_repo]$ git add -p
diff --git a/test_file.py b/test_file.py
index 093dd14..46446e5 100644
--- a/test_file.py
+++ b/test_file.py
@@ -1 +1,3 @@
-print("Goodbye, World :(")
+print('New First Line')
+print('Goodbye, World :(')
+print('New Last Line')
Stage this hunk [y,n,q,a,d,/,e,?]? 
[talk_repo]$ git commit -am"adding a chunk"
[master 08f56bf] adding a chunk
```

-----------

# .gitignore

```
[talk_repo]$ python -m cProfile -o profile.out test_file.py 
New First Line
Goodbye, World :(
New Last Line
[talk_repo]$ ls
profile.out  test_file.py
[talk_repo]$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

        profile.out

nothing added to commit but untracked files present (use "git add" to track)
```

-------------

```
[talk_repo]$ echo 'profile.out' > .gitignore
[talk_repo]$ git status
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)

        .gitignore

nothing added to commit but untracked files present (use "git add" to track)
[talk_repo]$ git add .gitignore 
[talk_repo]$ git commit -m"Add gitignore"
[master 604f56f] Add gitignore
 1 file changed, 1 insertion(+)
 create mode 100644 .gitignore
[talk_repo]$ git status
On branch master
nothing to commit, working tree clean
[talk_repo]$ ls
profile.out  test_file.py
```

--------------

# git stash (not Atlassian Stash)

```
[talk_repo]$ echo 'print("Real Last line")' >> test_file.py 
[talk_repo]$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   test_file.py

no changes added to commit (use "git add" and/or "git commit -a")
```

---------

```
[talk_repo]$ git stash
Saved working directory and index state WIP on master: 604f56f Add gitignore
[talk_repo]$ git status
On branch master
nothing to commit, working tree clean
[talk_repo]$ cat test_file.py 
print('New First Line')
print('Goodbye, World :(')
print('New Last Line')
```


---------

```
[talk_repo]$ git stash pop
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   test_file.py

no changes added to commit (use "git add" and/or "git commit -a")
Dropped refs/stash@{0} (008c9358492ccc273d2ddb87150d0d785cd820bd)
[talk_repo]$ cat test_file.py 
print('New First Line')
print('Goodbye, World :(')
print('New Last Line')
print("Real Last line")
[talk_repo]$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   test_file.py

no changes added to commit (use "git add" and/or "git commit -a")
[talk_repo]$ git commit -am"Add the real final line"
[master b2a7440] Add the real final line
 1 file changed, 1 insertion(+)

```

----------

# git log

```
[talk_repo]$ git log
commit b2a7440a79b2d9dbb43b06da24538b5ae8884817 (HEAD -> master)
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:23:49 2017 -0800

    Add the real final line

commit 604f56f1938c60f3f404a575da9ae6fcce35ad1f
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:16:03 2017 -0800

    Add gitignore

commit 08f56bf2a3ead2b5497c4c53884947ea4a6b065c
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:13:00 2017 -0800

    adding a chunk

commit 4ca471fb3d8f355e15fc978fb11bc9c9e0f5aab1
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:09:02 2017 -0800

    Adding test file
```


------


```
[talk_repo]$ git log -p
commit b2a7440a79b2d9dbb43b06da24538b5ae8884817 (HEAD -> master)
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:23:49 2017 -0800

    Add the real final line

diff --git a/test_file.py b/test_file.py
index 46446e5..e2c0c1d 100644
--- a/test_file.py
+++ b/test_file.py
@@ -1,3 +1,4 @@
 print('New First Line')
 print('Goodbye, World :(')
 print('New Last Line')
+print(Last line)

commit 604f56f1938c60f3f404a575da9ae6fcce35ad1f
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:16:03 2017 -0800

    Add gitignore

diff --git a/.gitignore b/.gitignore
new file mode 100644
index 0000000..134a1a2
--- /dev/null
+++ b/.gitignore
@@ -0,0 +1 @@
+profile.out

commit 08f56bf2a3ead2b5497c4c53884947ea4a6b065c
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:13:00 2017 -0800

    adding a chunk

diff --git a/test_file.py b/test_file.py
index 093dd14..46446e5 100644
```

-------

# git blame (but don't really blame, that's not nice)

```
[talk_repo]$ git blame test_file.py 
08f56bf2 (Alec Deason 2017-12-08 11:13:00 -0800 1) print('New First Line')
08f56bf2 (Alec Deason 2017-12-08 11:13:00 -0800 2) print('Goodbye, World :(')
08f56bf2 (Alec Deason 2017-12-08 11:13:00 -0800 3) print('New Last Line')
b2a7440a (Alec Deason 2017-12-08 11:23:49 -0800 4) print(Last line)
```

----

# squash

```
[talk_repo]$ git rebase -i 4ca471fb3d8f355e15fc978fb11bc9c9e0f5aab1
pick 08f56bf adding a chunk
pick 604f56f Add gitignore
pick b2a7440 Add the real final line

# Rebase 4ca471f..b2a7440 onto 4ca471f (3 commands)
#
# Commands:
# p, pick = use commit
# r, reword = use commit, but edit the commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like "squash", but discard this commit's log message
# x, exec = run command (the rest of the line) using shell
# d, drop = remove commit
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
```

-------

```
pick 08f56bf adding a chunk
s 604f56f Add gitignore
s b2a7440 Add the real final line
```

----

```
These are all of my changes
```

-----

```
[talk_repo]$ git log
commit a76c7cdb40a5d73d2b8461b91344fcb0554a83be (HEAD -> master)
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:13:00 2017 -0800

    These are all my changes

commit 4ca471fb3d8f355e15fc978fb11bc9c9e0f5aab1
Author: Alec Deason <alecwd@uw.edu>
Date:   Fri Dec 8 11:09:02 2017 -0800

    Adding test file
```
