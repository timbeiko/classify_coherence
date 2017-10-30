import json 
from random import randint, sample
from collections import defaultdict

# Variables 
data = []          
connectives = []    

# Input
relations_json =                                   'data/relations-01-12-16-train.json'
# Output files 
coherent_sentences_file =                          'data/json/coherent_sentences.json'
incoherent_sentences_arg2_random =                 'data/json/incoherent_sentences_arg2_random.json'
incoherent_sentences_connective_random =           'data/json/incoherent_sentences_connective_random.json'
incoherent_sentences_arg2_same_sense =             'data/json/incoherent_sentences_arg2_same_sense.json'
incoherent_sentences_arg2_diff_sense =             'data/json/incoherent_sentences_arg2_diff_sense.json'
incoherent_sentences_arg2_matching_connectives =   'data/json/incoherent_sentences_arg2_matching_connectives.json'
incoherent_sentences_connective_diff_sense =       'data/json/incoherent_sentences_connective_diff_sense.json'

# Helper methods 
def output_sentences(sentences, output_file):
    open(output_file, 'w') # Clear contents of file 
    # Write sentences to output files 
    with open(output_file, 'a+') as out:
        for sentence in sentences:
            json.dump(sentence, out)
            out.write('\n')

def create_sentence(arg1, arg2, connective, sense):
    sentence = {
        'Arg1Raw': arg1.lower(),
        'Arg2Raw': arg2.lower(),
        'ConnectiveRaw': connective.lower(),
        'Sense': sense.lower(),
    }
    return sentence

# Import relations data as a JSON object 
for line in open(relations_json, 'r'):
    data.append(json.loads(line))

# Only keep top level Sense
for line in data:
    top_level_sense = ""
    for sense in line['Sense']:
        split_sense = sense.split('.', 1)
        top_level_sense = split_sense[0]
    line['Sense'] = top_level_sense

# Remove sentences with Explicit connectives 
data = filter(lambda line: line['Type'] != 'Explicit', data)
# Remove sentences with "" as Connective
data = filter(lambda line: line['Connective']['RawText'] != '', data)
data = filter(lambda line: line['Connective']['RawText'] != "", data)

# Coherent sentences
coherent_sentences = []
for line in data:
    coherent_sentences.append(create_sentence(line['Arg1']['RawText'], 
                                              line['Arg2']['RawText'], 
                                              line['Connective']['RawText'], 
                                              line['Sense']))
    # Store 'arg2s' and 'connectives' to create incoherent sentences afterwards
    connective = {line['Connective']['RawText']: line['Sense']}
    connectives.append(connective)
output_sentences(coherent_sentences, coherent_sentences_file)

# Create a set of unique connectives and their senses
unique_connectives_senses = {}
for i in iter(connectives):
    for c, s in i.items():
        if c not in unique_connectives_senses:
            unique_connectives_senses[c] = [s]
        elif s not in unique_connectives_senses[c]:
            unique_connectives_senses[c].append(s)

# RANDOM: Incoherent sentences by swapping Arg2s
incoherent_sentences = []
coherent_copy = list(coherent_sentences)
for line in data:
    # Get a random sentence 
    index = randint(0, len(coherent_copy)-1)
    random_cohenrent_sentence = coherent_copy[index] 

    coherent_copy.pop(index) # Remove sentence with used Arg2 from set of sentences
    incoherent_sentences.append(create_sentence(line['Arg1']['RawText'],
                                                random_cohenrent_sentence['Arg2Raw'],
                                                line['Connective']['RawText'],
                                                line['Sense']))
output_sentences(incoherent_sentences, incoherent_sentences_arg2_random)

# RANDOM: Incoherent sentences by swapping connectives
incoherent_sentences = []
for line in data:
    # Get a random connective
    connective_list = sample(unique_connectives_senses, 1)
    connective = connective_list[0]
    incoherent_sentences.append(create_sentence(line['Arg1']['RawText'],
                                                line['Arg2']['RawText'],
                                                connective,
                                                next(iter(unique_connectives_senses[connective])))) # Issue: this will always be the first element (thus the first possible Sense)
output_sentences(incoherent_sentences, incoherent_sentences_connective_random)

# SAME SENSE: Incoherent sentences by swapping Arg2s
incoherent_sentences = []
coherent_copy = list(coherent_sentences)
for line in data:
    # Get a random sentence 
    index = randint(0, len(coherent_copy)-1)
    random_cohenrent_sentence = coherent_copy[index] 

    # Ensure that connection between Arg1 and new Arg2 is the same as connection between Arg1 and original Arg2
    # Because this may not be possible for all sentences, we will try a maximum of 1000 times.
    tries = 0 
    while (random_cohenrent_sentence['Sense'] not in unique_connectives_senses[line['Connective']['RawText']] and tries < 1000):
        index = randint(0, len(coherent_copy)-1)
        random_cohenrent_sentence = coherent_copy[index] 
        tries += 1
    tries = 0 
    coherent_copy.pop(index) # Remove sentence with used Arg2 from set of sentences
    incoherent_sentences.append(create_sentence(line['Arg1']['RawText'],
                                                random_cohenrent_sentence['Arg2Raw'],
                                                line['Connective']['RawText'],
                                                line['Sense']))
output_sentences(incoherent_sentences, incoherent_sentences_arg2_same_sense)

# DIFFERENT SENSE: Incoherent sentences by swapping Arg2s
incoherent_sentences = []
coherent_copy = list(coherent_sentences)
for line in data:
    # Get a random sentence that is not the same as the current one
    index = randint(0, len(coherent_copy)-1)
    random_cohenrent_sentence = coherent_copy[index] 

    # Ensure that connection between Arg1 and new Arg2 is not the same as connection between Arg1 and original Arg2
    # Because this may not be possible for all sentences, we will try a maximum of 1000 times.
    tries = 0 
    while (random_cohenrent_sentence['Sense'] in unique_connectives_senses[line['Connective']['RawText']] and tries < 1000):
        index = randint(0, len(coherent_copy)-1)
        random_cohenrent_sentence = coherent_copy[index] 
        tries += 1
    tries = 0 
    coherent_copy.pop(index) # Remove sentence with used Arg2 from set of sentences
    incoherent_sentences.append(create_sentence(line['Arg1']['RawText'],
                                                random_cohenrent_sentence['Arg2Raw'],
                                                line['Connective']['RawText'],
                                                line['Sense']))
output_sentences(incoherent_sentences, incoherent_sentences_arg2_diff_sense)

# MATCHING CONNECTIVE: Incoherent sentences by swapping Arg2s
incoherent_sentences = []
coherent_copy = list(coherent_sentences)
for line in data:
    # Get a random sentence that is not the same as the current one
    index = randint(0, len(coherent_copy)-1)
    random_cohenrent_sentence = coherent_copy[index] 

    # Ensure that connection between Arg1 and new Arg2 is the same as connection between Arg1 and original Arg2
    # Because this may not be possible for all sentences, we will try a maximum of 1000 times.
    tries = 0 
    while (random_cohenrent_sentence['ConnectiveRaw'] != line['Connective']['RawText'] and tries < 1000):
        index = randint(0, len(coherent_copy)-1)
        random_cohenrent_sentence = coherent_copy[index] 
        tries += 1
    if tries == 1000:
        continue
    tries = 0 

    coherent_copy.pop(index) # Remove sentence with used Arg2 from set of sentences
    incoherent_sentences.append(create_sentence(line['Arg1']['RawText'],
                                                random_cohenrent_sentence['Arg2Raw'],
                                                line['Connective']['RawText'],
                                                line['Sense']))
output_sentences(incoherent_sentences, incoherent_sentences_arg2_matching_connectives)

# DIFFERENT SENSE CONNECTIVE: Incoherent sentences by swapping connectives
incoherent_sentences = []
for line in data:
    # Get a random connective
    connective_list = sample(unique_connectives_senses, 1)
    connective = connective_list[0]

    # Ensure connective does not have the same sense as the original
    while (line['Sense'] in unique_connectives_senses[connective]):
        connective_sample = sample(unique_connectives_senses, 1)
        connective = connective_sample[0]
    incoherent_sentences.append(create_sentence(line['Arg1']['RawText'],
                                                line['Arg2']['RawText'],
                                                connective,
                                                next(iter(unique_connectives_senses[connective]))))
output_sentences(incoherent_sentences, incoherent_sentences_connective_diff_sense)
