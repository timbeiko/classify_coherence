import os 
import nltk 
import json 
import random
import numpy as np 

# Coherent sentences
coherent_file = 'coherent_sentences.json'
file_content = []
for line in open("data/json/" + coherent_file, 'r'):
    file_content.append(json.loads(line))


outfile = "data/random/coherent_sentences.txt"
open(outfile, 'w') # Clear contents of file 
coherent_output = open(outfile, 'a+')

for line in file_content:
    Arg1 = nltk.word_tokenize(line['Arg1Raw'].lower()) 
    Arg2 = nltk.word_tokenize(line['Arg2Raw'].lower())
    Conn = nltk.word_tokenize(line['ConnectiveRaw'].lower())
    sentence = " ".join(Arg1) + " " + " ".join(Conn) + " " + " ".join(Arg2) + "\n"
    coherent_output.write(sentence.encode('ascii', 'ignore'))


# Incoherent sentences
file_content = []
file_to_randomize = 'incoherent_sentences_arg2_diff_sense.json'
gammas = np.arange(0.0, 1.1,0.1)
for line in open("data/json/" + file_to_randomize, 'r'):
    file_content.append(json.loads(line))

for gamma in gammas: 
    outfile = "data/random/{}_gamma_{:g}.txt".format(file_to_randomize[:-5], gamma)
    open(outfile, 'w') # Clear contents of file 
    randomized_file = open(outfile, 'a+')

    for line in file_content:
        Arg1 = nltk.word_tokenize(line['Arg1Raw'].lower()) 
        Arg2 = nltk.word_tokenize(line['Arg2Raw'].lower())
        Conn = nltk.word_tokenize(line['ConnectiveRaw'].lower())

        words_to_shuffle = []
        Arg2_index_shuffle = [False]*len(Arg2)

        for i, word in enumerate(Arg2):
            if random.uniform(0,1) < gamma: 
                words_to_shuffle.append(word)
                Arg2_index_shuffle[i] = True

        shuffled_Arg2 = []

        if len(words_to_shuffle) > 1:
            for i, word in enumerate(Arg2):
                if Arg2_index_shuffle[i] == True:
                    replacement_word = random.choice(words_to_shuffle)

                    # Ensure replacement word is not the same as the initial word
                    tries = 0 
                    while replacement_word == word and tries < 100:
                        replacement_word = random.choice(words_to_shuffle)
                        tries += 1

                    shuffled_Arg2.append(replacement_word)
                    words_to_shuffle.remove(replacement_word)
                else:
                    shuffled_Arg2.append(word)
        else:
            shuffled_Arg2 = Arg2


        sentence = " ".join(Arg1) + " " + " ".join(Conn) + " " + " ".join(shuffled_Arg2) + "\n"
        randomized_file.write(sentence.encode('ascii', 'ignore'))