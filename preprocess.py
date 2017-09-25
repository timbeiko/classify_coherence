import json 
from random import randint, sample
from collections import defaultdict

# Variables 
data = []          
connectives = []    

# Output files 
relations_json =                              'data/relations-01-12-16-dev.json'
coherent_output =                             'data/coherent-sentences.json'
incoherent_output_arg2_random =               'data/arg2-random-incoherent-sentences.json'
incoherent_output_arg2_diff_sense =             'data/arg2-different-sense-incoherent-sentences.json'
incoherent_output_arg2_same_sense =             'data/arg2-same-sense-incoherent-sentences.json'
incoherent_output_arg2_matching_connectives = 'data/arg2-matching-connective-incoherent-sentences.json'
incoherent_output_connective_random =         'data/connective-random-incoherent-sentences.json'
incoherent_output_connective_filtered =       'data/connective-filtered-incoherent-sentences.json'

# Helper methods 
def output_sentences(sentences, output_file):
    open(output_file, 'w') # Clear contents of file 

    # Write sentences to output files 
    with open(output_file, 'a+') as out:
        for sentence in sentences:
            json.dump(sentence, out)
            out.write('\n')

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

# Remove sentences with Implicit connectives 
data = filter(lambda line: line['Type'] != 'Explicit', data)

output_sentences(data, "implicit.txt")

# Coherent sentences
coherent_sentences = []
for line in data:
    sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': line['Arg2']['RawText'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }
    coherent_sentences.append(sentence)

    # Store 'arg2s' and 'connectives' to create incoherent sentences afterwards
    connective = {line['Connective']['RawText']: line['Sense']}
    connectives.append(connective)

# Write coherent sentences to output files 
output_sentences(coherent_sentences, coherent_output)

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
    # Get a random sentence that is not the same as the current one
    index = randint(0, len(coherent_copy)-1)
    random_cohenrent_sentence = coherent_copy[index] 

    coherent_copy.pop(index) # Remove sentence with used Arg2 from set of sentences

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': random_cohenrent_sentence['Arg2Raw'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }
    
    incoherent_sentences.append(incoherent_sentence)
# Write incoherent sentences to output files 
output_sentences(incoherent_sentences, incoherent_output_arg2_random)

# WITH FILTERING: Incoherent sentences by swapping Arg2s (different sense)
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

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': random_cohenrent_sentence['Arg2Raw'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }

    incoherent_sentences.append(incoherent_sentence)
# Write incoherent sentences to output files 
output_sentences(incoherent_sentences, incoherent_output_arg2_diff_sense)

# WITH FILTERING: Incoherent sentences by swapping Arg2s (same sense)
incoherent_sentences = []
coherent_copy = list(coherent_sentences)
for line in data:
    # Get a random sentence that is not the same as the current one
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

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': random_cohenrent_sentence['Arg2Raw'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }

    incoherent_sentences.append(incoherent_sentence)
# Write incoherent sentences to output files 
output_sentences(incoherent_sentences, incoherent_output_arg2_same_sense)

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

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': random_cohenrent_sentence['Arg2Raw'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }

    incoherent_sentences.append(incoherent_sentence)
# Write incoherent sentences to output files 
output_sentences(incoherent_sentences, incoherent_output_arg2_matching_connectives)

# RANDOM: Incoherent sentences by swapping connectives
incoherent_sentences = []
for line in data:
    # Get a random connective
    connective_list = sample(unique_connectives_senses, 1)
    connective = connective_list[0]

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': line['Arg2']['RawText'],
        'ConnectiveRaw': connective,
        'Sense': next(iter(unique_connectives_senses[connective])), # Issue: this will always be the first element (thus the first possible Sense)
    }
    incoherent_sentences.append(incoherent_sentence)
# Write incoherent sentences to output files 
output_sentences(incoherent_sentences, incoherent_output_connective_random)

# WITH FILTERING: Incoherent sentences by swapping connectives
incoherent_sentences = []
for line in data:
    # Get a random connective
    connective_list = sample(unique_connectives_senses, 1)
    connective = connective_list[0]

    # Ensure connective does not have the same sense as the original
    while (line['Sense'] in unique_connectives_senses[connective]):
        connective_sample = sample(unique_connectives_senses, 1)
        connective = connective_sample[0]

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': line['Arg2']['RawText'],
        'ConnectiveRaw': connective,
        'Sense': next(iter(unique_connectives_senses[connective])), # Issue: this will always be the first element (thus the first possible Sense)
    }
    incoherent_sentences.append(incoherent_sentence)
# Write incoherent sentences to output files 
output_sentences(incoherent_sentences, incoherent_output_connective_filtered)
