# Undo commit to the wrong branch (DRAFT)

Made an interest mistake the other day. I've commited a bunch of files to the wrong branch. On my hasty attempt to fix it I ended up doing another
larger mistake and lost the work. Fortunately it wasn't a big piece. 
What was the mistake and what's the right way of going about doing this?

# Setup

Let's create a small git repo so we can play along.

# The mistake

```
git revert
git reset --soft HEAD~2
```


## The right way of fixing this

Run the following right after commiting, assuming you didn't push.

```
git reset --soft HEAD^
git checkout branch
git commit
```
