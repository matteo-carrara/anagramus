# anagramus
Quick anagram generator
_by matteo carrara_

# How to run
Clone/download the repository, then you shall run

```
 python .\anagram.py
```

inside the same directory as *italiano.txt* since it will be loaded at run time (currentyly this program only supports italian words). 

# Example

```
> python .\anagram.py "beato coi libri"
Loading dictionary
Dict loaded, rows =  4261421
Elapsed time: 1.344862461090088 seconds
Calculating frequencies for dictionary...
Words with not allowed symbols will be skipped
Done
Elapsed time: 23.183022260665894 seconds
Starting to search for words
COMPLETE ANAGRAM FOUND!!!!!! bibliotecario
Insert another word:
```


## What is an anagram?
Regarding this software, an anagram is defined as follows:
an anagram of a word or a phrase T is a permutation of all characters of T (excluding spaces), that contains one or more words from a specific language AND uses every single character of T (so that the anagram can be reversed back to the original form).

To check if a word/combination of words is an anagram of another word/set of words, there is included a script "is_anagram" to check it.
