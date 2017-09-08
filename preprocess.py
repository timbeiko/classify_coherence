import json 
from random import randint

# Importing relations data as a JSON object 
data = []
for line in open('data/relations-01-12-16-dev.json', 'r'):
    data.append(json.loads(line))

# Clear data from output files
open('data/coherent-sentences.json', 'w') 
open('data/arg2-incoherent-sentences.json', 'w') 

arg2s = [] # To be used to create incoherent sentences 

# Creating coherent sentences
# Get Arg1, Arg2, Connective and Sense from each sample
for line in data:
    if (line['Type'] == 'Implicit'):
        continue

    sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': line['Arg2']['RawText'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }

    arg2s.append(line['Arg2']['RawText'])

    # Write coherent sentences to output files 
    with open('data/coherent-sentences.json', 'a+') as output_file:
        json.dump(sentence, output_file)
        output_file.write('\n')


# Creating incoherent sentences by swapping Arg2s
for line in data:
    if (line['Type'] == 'Implicit'):
        continue

    # Get a random Arg2
    index = randint(0, len(arg2s)-1)
    incoherentArg2 = arg2s[index]

    # In case we get the original Arg2
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

