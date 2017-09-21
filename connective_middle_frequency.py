import json 
import os 

# Variables 
data = []          
connectives = {}    

for filename in os.listdir(os.getcwd()+ "/data"):
    if "relations" not in filename: 
        continue

    # Import relations data as a JSON object 
    for line in open("data/" + filename, 'r'):
        data.append(json.loads(line))

    # Remove sentences with implicit connectives
    data = filter(lambda line: line['Type'] != 'Implicit', data)

    for line in data:
        # Get end of Arg1
        arg1_chars = line['Arg1']['CharacterSpanList']
        arg1_end   = arg1_chars[len(arg1_chars)-1][1]

        # Get start of Arg2
        arg2_chars = line['Arg2']['CharacterSpanList']
        arg2_start = arg2_chars[len(arg2_chars)-1][0]

        # Get start and end of Connective
        conn_chars = line['Connective']['CharacterSpanList']
        if len(conn_chars) == 0: # Probably errors in dataset, because some 
            continue
        conn_start = conn_chars[len(conn_chars)-1][0]
        conn_end   = conn_chars[len(conn_chars)-1][1]

        # Identify 'middle connective'
        if (arg1_end < conn_start) and (conn_end < arg2_start):
            connectives['TOTAL'] = connectives.get('TOTAL', 0) + 1
            connectives[line['Connective']['RawText'].lower()] = connectives.get(line['Connective']['RawText'].lower(), 0) + 1

output_file = "data/txt/middle_connective_frequency.txt"
open(output_file, 'w') # Clear contents of file 
out = open(output_file, 'a+')
for connective in sorted(connectives, key=connectives.get):
    s = connective + ": " + str(connectives[connective]) + "\n"
    out.write(s)


