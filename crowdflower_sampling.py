import os
import random
import csv

CROWDFLOWER_DIR = "crowdflower_data"

open(CROWDFLOWER_DIR + "/samples.csv", 'w') # Clear contents of file 
# Get txt version of data 
with open(CROWDFLOWER_DIR + "/samples.csv", 'a+') as csvfile:
    writter = csv.writer(csvfile)
    writter.writerow(["Dataset", "Sample"])
    for filename in os.listdir(os.getcwd()+ "/data/txt"):
        if filename in [".keep", "coherent_sentences.txt"]:
            continue

        filepath = "data/txt/" + filename
        num_lines = sum(1 for line in open(filepath, 'r'))

        # Randomly get 101 lines in the file
        sample_lines = random.sample(range(1, num_lines), 51)
        i = 0 
        for line in open(filepath, 'r'):
            if i in sample_lines:
                writter.writerow([filename, line])
                sample_lines.remove(i)
            i += 1

            


