import json 

# Importing relations data as a JSON object 
data = []
for line in open('data/relations-01-12-16-dev.json', 'r'):
    data.append(json.loads(line))

# Clear content from output file
open('data/coherent-sentences.json', 'w') 

# Get Arg1, Arg2, Connective and Sense from each sample
for line in data:
    sentence = {
        'Arg1Raw': line['Arg1']['RawText'],
        'Arg2Raw': line['Arg2']['RawText'],
        'ConnectiveRaw': line['Connective']['RawText'],
        'Sense': line['Sense'],
    }

    # Write coherent sentences to output files 
    with open('data/coherent-sentences.json', 'a+') as output_file:
        json.dump(sentence, output_file)
        output_file.write('\n')