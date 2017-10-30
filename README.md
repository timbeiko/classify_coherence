# Classify Coherence
An attempt to classify sentences from the Penn Discourse Treebank as either coherent or incoherent. 

### Getting Started
To get started,  you will need to add a PDTB `relations-XX-XX-XX-{dev | train | test}.json` file to the `/data` directory, and update the value of `relations_json` in `generate_sentences.py` (declared around line 10) to the name of that file. 
In order to train with the Google News word2vec embeddings, you will need to download them (available here: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM), and unzip them in the `\model` directory. 

### [in progress] Detailed Report
A detailled (in progress) report of this project can be found at https://www.overleaf.com/read/ngfcbdxkcgby

