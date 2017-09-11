import json 
from random import randint, sample
from collections import defaultdict

# Importing relations data as a JSON object 
data = []
for line in open('data/relations-01-12-16-dev.json', 'r'):
    data.append(json.loads(line))

# Clear data from output files
open('data/coherent-sentences.json', 'w') 
open('data/arg2-incoherent-sentences.json', 'w') 
open('data/connective-incoherent-sentences.json', 'w') 

# Used to create incoherent sentences 
arg2s = [] 
connectives = [] 

# Remove sentences with Implicit connectives 
data = filter(lambda line: line['Type'] != 'Implicit', data)

# Creating coherent sentences
# Get Arg1, Arg2, Connective and Sense from each sample
for line in data:
    sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': line['Arg2']['RawText'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }

    # Storing 'arg2s' and 'connectives' to create incoherent sentences afterwards
    arg2s.append(line['Arg2']['RawText'])

    connective = {line['Connective']['RawText']: []}
    for i in iter(line['Sense']):
        connective[line['Connective']['RawText']].append(i)
    connectives.append(connective)

    # Write coherent sentences to output files 
    with open('data/coherent-sentences.json', 'a+') as output_file:
        json.dump(sentence, output_file)
        output_file.write('\n')

# Creating incoherent sentences by swapping Arg2s
for line in data:
    # Get a random Arg2
    index = randint(0, len(arg2s)-1)
    incoherentArg2 = arg2s[index]

    # Ensure we do not get the original Arg2
    while (incoherentArg2 == line['Arg2']['RawText']):
        index = randint(0, len(arg2s)-1)
        incoherentArg2 = arg2s[index]

    arg2s.pop(index) 

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': incoherentArg2,
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }

    # Write incoherent sentences to output files 
    with open('data/arg2-incoherent-sentences.json', 'a+') as output_file:
        json.dump(incoherent_sentence, output_file)
        output_file.write('\n')


# Create a set of unique connectives 
unique_connectives = {}
for i in iter(connectives):
    for c, s in i.items():
        if c not in unique_connectives:
            unique_connectives[c] = []
        for i in iter(s):
            unique_connectives[c].append(i)

# Remove duplicate senses from each connectives 
for c, s, in unique_connectives.items():
    unique_connectives[c] = set(s)

# Create incoherent sentences by swapping connectives
for line in data:
    # Get a random connective
    connective_list = sample(unique_connectives, 1)
    connective = connective_list[0]

    while ( # Ensure connective is not the same as the original
            (connective == line['Connective']['RawText']) or 
            # Ensure connective is does not have the same sense as the original
            (len(unique_connectives[connective].intersection(set(line['Sense']))) != 0)
        ):
        connective_list = sample(unique_connectives, 1)
        connective = connective_list[0]

    incoherent_sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': line['Arg2']['RawText'],
        'ConnectiveRaw': connective,
        'Sense': next(iter(unique_connectives[connective])), # Issue: this will always be the first element (thus the first possible Sense)
    }

    # Write incoherent sentences to output files 
    with open('data/connective-incoherent-sentences.json', 'a+') as output_file:
        json.dump(incoherent_sentence, output_file)
        output_file.write('\n')
