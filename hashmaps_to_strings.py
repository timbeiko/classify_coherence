# This takes the output of preprocess.py and converts it to raw text
# While also keeping track of sentence lengths and creating a dictionary of words 
import os 
import nltk 
import json 

dictionary = {}
max_sentence_length = 0 

for filename in os.listdir(os.getcwd()+ "/data"):
    # Skip input data to preprocess.py and generated .txt files 
    if "relations" in filename or "json" not in filename: 
        continue


    # Import data as a JSON object 
    data = []
    for line in open("data/" + filename, 'r'):
        data.append(json.loads(line))

    output_file = "data/txt/" + filename[:-5] + ".txt"
    open(output_file, 'w') # Clear contents of file 
    out = open(output_file, 'a+')

    for line in data:
        sentence = line['Arg1Raw'] + " " + line['ConnectiveRaw'] + " " + line['Arg2Raw'] + "\n"
        out.write(sentence)

        word_sentence = nltk.word_tokenize(sentence.lower())
        if len(word_sentence) > max_sentence_length:
            max_sentence_length = len(word_sentence)
        for word in word_sentence:
            if word not in dictionary:
                dictionary[word] = 1
            else:
                dictionary[word] += 1 

print len(dictionary.keys())
print max_sentence_length
