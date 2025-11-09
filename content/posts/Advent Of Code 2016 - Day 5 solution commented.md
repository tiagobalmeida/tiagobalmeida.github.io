+++
title = "Advent of Code 2016 Day 5 Solution Commented"
date = "2017-01-17T15:26:47+01:00"
#dateFormat = "2006-01-02" # This value can be configured for per-post date formatting
author = ""
authorTwitter = "" #do not include @
cover = ""
tags = ["programming", "clojure"]
keywords = ["", ""]
description = ""
showFullContent = false
readingTime = false
hideComments = false
+++

# Advent Of Code 2016 - Day 5 solution commented

## The problem
The original problem, with an amusing tale for motivation can be found [here](http://adventofcode.com/2016/day/5). 
For the purposes of this it is sufficient to know the following:

You arrive at a password protected door with ID 'uqwqemis'.

The eight-character password for the door is generated one character at a time by finding the MD5 hash of some Door ID (the puzzle input) and an increasing integer index (starting with 0).

A hash indicates the next character in the password if its hexadecimal representation starts with five zeroes. If it does, the sixth character in the hash is the next character of the password.

For example, if the Door ID is abc:

The first index which produces a hash that starts with five zeroes is 3231929, which we find by hashing abc3231929; the sixth character of the hash, and thus the first character of the password, is 1.
5017308 produces the next interesting hash, which starts with 000008f82..., so the second character of the password is 8.
The third time a hash starts with five zeroes is for abc5278568, discovering the character f.
In this example, after continuing this search a total of eight times, the password is 18f47a30.

## My solution overview

The problem can be solved by taking the fixed input ID and successively trying different integers, increasing from 0. 

So, we want to compute
- MD5(door_ID,0)
- MD5(door_ID,1)
- MD5(door_ID,2)
- ...

For each one we check if it starts with five zeroes. If it does we append the sixth char of the hash into the password. 

The process stops when the password has 8 characters.

As an additional challenge, i've decided to try implementing this in Clojure. A lisp-like language that runs on the JVM. It was my first experience with the language.

## Commented solution
The whole code for the solution can be found [here](https://github.com/jumpifzero/adventofcode2016/blob/master/day5/src/app/core.clj)

The general process is this:

Start with a lazy list of successive integers from 0.
For each one, prepend the door ID. This is a good problem for a map, which produces another list.
From this list of door_ID,Counter we use a map for getting the corresponding items md5 hashes. 

In clojure this is done for instance with:
```lisp
(map digest/md5 
	(map (fn [s] (str door-id-str s)) 
		(range)))
```
Reading inside-out we have (range) that produces a list of integers from 0.
str is a function that produces a string, essentially concatenating door-id-str with its argument s. This anonymous function (fn) is used on the inner map to produce a list of door_ID,Counter for all values of Counter from 0 to above.

This is fed into a second map with a library function digest/md5 to get the md5 hashes of those strings.

**Isn't this an infinite list??**

It is! If you tried to print the result of the expression above, it would go on forever as it is using all integers from 0 until infinity. The beauty is that (range) doesn't actually return such a list. Instead, it returns _something_ that knows how to get the next element in the sequence. This is called a lazy sequence in many languages.
Further down you'll see how the process stops.

So now, we have a list of hashes. We'll need to process it one item a time and in order. 

For each item, we see if it starts with five zeroes. When it does, we get the sixth char, when it does not, we just skip it. We can stop looking at items in the list when the resulting password is already 8 chars long.

There are many ways to do this. A simple for loop would work. Instead I went with a reduce, which is a common pattern for taking a sequence and another function f, apply f to successive pairs of elements in the sequence and return a single element. _Reduce_ the sequence into one thing.

This is done in the following bit of code:

```lisp
(reduce 
    (fn [password token] 
      (if (= (count password) 8)
        (reduced password)
        (if (= (subs token 0 5) "00000")
          (str password (subs token 5 6)) 
          password)))
	""
	list_of_md5_hashes
```

Let's break it down.


The general pattern we want is `(reduce process_item_function initial_password list_of_md5_hashes)`.

- initial_password is an empty string (we don't know any password character yet!). This is the "" above.
- list_of_md5_hashes is what we got earlier with the maps.
- process_item_function is a function that will get the password we got so far, and an item from the list (here called token). It needs to do two things:
    1. See if the password is already 8 chars long. If it is break the outer reduce with it (our overall result): `(reduced password)`
    2. See if the token starts with five zeroes. When it does, return the password we know with the sixth char of this token appended. `(if (= (subs token 0 5) "00000") ...`


## Final remarks

Really like how clojure makes this solution very short and readable. The whole thing is 33 lines with empty lines and comments.

## Admin
Last updated at 16/01/2017