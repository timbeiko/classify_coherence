# Classify Coherence
An attempt to classify sentences from the Penn Discourse Treebank as either coherent or incoherent. 

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