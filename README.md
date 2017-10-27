# Classify Coherence
An attempt to classify sentences from the Penn Discourse Treebank as either coherent or incoherent. 

## TODO
- word2vec embeddings 

### Getting Started
Hopefully, everything should run and there should be no funky dependencies. 
Because the PDTB data is not available freely, it has not been uploaded to this repo. 

For the code to run, you will need a data folder with the following subdirectories:

```
data/integers
    /json
    /padded
    /txt
```
Once you have these, you will need to add a PDTB `relations-XX-XX-XX-{dev | train | test}.json` file to the `/data` directory, and update the value of `relations_json` in `generate_sentences.py` (declared around line 10) to the name of that file. 

### [in progress] Detailed Report
A detailled (in progress) report of this project can be found at https://www.overleaf.com/read/ngfcbdxkcgby

#### Notes

- To get a single parsed sentence from 'parses.json', read it into 'data' and then: `data[0]['wsj_2276']['sentences'][0]`
- CNN Model built from https://github.com/dennybritz/cnn-text-classification-tf
- To analyze TF vocabulary:
```
import numpy as np
from tensorflow.contrib import learn

x_text = ['This is a cat','This must be boy', 'This is a a dog']
max_document_length = max([len(x.split(" ")) for x in x_text])

## Create the vocabularyprocessor object, setting the max lengh of the documents.
vocab_processor = learn.preprocessing.VocabularyProcessor(max_document_length)

## Transform the documents using the vocabulary.
x = np.array(list(vocab_processor.fit_transform(x_text)))    

## Extract word:id mapping from the object.
vocab_dict = vocab_processor.vocabulary_._mapping

## Sort the vocabulary dictionary on the basis of values(id).
## Both statements perform same task.
#sorted_vocab = sorted(vocab_dict.items(), key=operator.itemgetter(1))
sorted_vocab = sorted(vocab_dict.items(), key = lambda x : x[1])

## Treat the id's as index into list and create a list of words in the ascending order of id's
## word with id i goes at index i of the list.
vocabulary = list(list(zip(*sorted_vocab))[0])
``` 