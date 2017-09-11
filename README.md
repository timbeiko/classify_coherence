# Classify Coherence
An attempt to classify sentences from the Penn Discourse Treebank as either coherent or incoherent. 

### [in progress] Detailed Report
A detailled (in progress) report of this project can be found at https://www.overleaf.com/read/ngfcbdxkcgby

### Goal of project
An assumption in a lot of NLP work is that the input text is coherent, but that may not always be true. My project will be to try and determine whether a sentence is coherent or not. To do this, I will use the PDTB data set, where sentences are broken down as Argument 1 (Arg1), Discourse Connector (DC) and Argument 2 (Arg2). On this data set, we will try two different experiments:

1) Swapping the Arg2s from each sentence with another to make the original sentence incoherent and:
  1a) Classifying coherent vs. incoherent sentences 
  1b) Identifying, from a set of n corrupted sentences and one valid sentence, the coherent one.

2) Swapping the DC from each sentence with another (ideally that does not imply the same discourse relation) to make the original sentence incoherent and:
  2a)  Classifying coherent vs. incoherent sentences 
  2b) Identifying, from a set of n corrupted sentences and one valid sentence, the coherent one.

#### PDTB Data
Because the PDTB Data set requires a license, it is not included in this repo. In order to run the code from this project and add this data, you will need to create a top-level folder named 'data' and include the PDTB data set there. This folder is also necessary to store the output of `preprocess.py`.

