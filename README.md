# BuckLang_CSCI341

BuckLang is a basic command language for programming two-way Turing machines covered in Bucknell's [CSCI 341 Theory of Computation course in Fall 2025](https://toddtoddtodd.net/courses/csci341/compiled/csci341_index.html).
It is based on the "WB" language taught as part of [Stanford's CS 203 Mathematical Foundations of Computing course taught in 2012](https://web.stanford.edu/class/archive/cs/cs103/cs103.1132/) (as well as other years). 

## How to Run It
First, clone the repository.
Run this in your terminal in the folder where you cloned it:
```
python3 bucklang.py sample_bucklang.buck "111000"
```
The first two are just running the python script. The last half tells it which bucklang script to run it on, and then what the input string should be.
If you choose to let it track, it will write to an output file. Otherwise, it will just print the result of runnning the program.

### Interactive Mode
You can also just run it on in interactive mode, where you just get the tape machine and tape programs to play around with. 
To do that, just run 
```
python3 bucklang.py
```

# Bucklang Workshop
If you are in CSCI341, you are probably beinng asked to take part in the workshop on programming Turing machines.
This entails visiting the [Gradescope submission page](https://www.gradescope.com/courses/1094390/assignments/7061812) and submitting your BuckLang programs and output files.
