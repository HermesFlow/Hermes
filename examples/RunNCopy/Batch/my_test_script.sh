#!/bin/bash

echo "Here is an example of a shell script"
echo "1a. File listing"
ls
echo ""

echo "1b. File listing with details (long format, just the first few lines)"
ls -l |head -n 5
echo ""

echo "2. Printing a calendar for the current month"
cal
echo ""

echo "3. Here's a little for loop"
n=1
for f in The quick brown fox jumps over the lazy dog; do
    echo "  Word number $n is $f"
    let n+=1
done
echo ""

echo 'Right, Im all done.  Bye bye.'
