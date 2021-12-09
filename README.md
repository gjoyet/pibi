## Programming in Bioinformatics - Block 3

### I. Setting up Environment and Running the Code

* Create the environment using the pibi_block3.yml file with the command:  
  + _conda env create -f pibi_block3.yml_
* Activate it the following way:
  + _conda activate pibi_
* Then run the code:
  + _python ex1.py_
  + _python ex2.py_

OR

* Run the batch script in order to also execute the STAR commands, tests, etc.:
  * _bash run_me.sh_


### II. Exercises

1. Answers:
* Sequence 3 contains a 'D', making it invalid, so it was discarded.  
* Sequence 1 and 2 are found on only one chromosome each.
* Sequence 4 on the other hand is found on three of the four chromosomes. However, this is likely due to its short size, rendering a hit not very meaningful.

2. Answers:
* \# of alignments: 108
* \# of uniquely mapped alignments: 0
* \# of multi-mapped alignments: 26
* The last point I did not know how to do, hence I can not say if the numbers match.

3. Remark:
* My code coverage is not quite 100% since the main methods are not tested.
However, I believe unit tests should not test them, which is why I left it as is.