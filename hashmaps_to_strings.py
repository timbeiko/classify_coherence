# This takes the output of preprocess.py and converts it to a format acceptable for Syntaxnet. 
import os 
import json 

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