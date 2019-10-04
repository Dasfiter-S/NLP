#import tensorflow as tf
import argparse
import glob
import json

#commandline options
def launch_options():
    parser = argparse.ArgumentParser("This program analyzes synonyms and returns the most\
                                  likely candidates that are similar to the word provided.")
    parser.add_argument('-s', '--synonym', help='Choose a word to analyze.', type=str)
    parser.add_argument('-f', '--file', help='You can load your own dictionary. Will have \
                        to recompute the tables however.', type=str)
    parser.add_argument('-r', '--recompute', help='Load default data file and compute\
                        again.', default=False)
    parser.add_argument('-m', '--merge', help="Merge dictionary files into single json\
                        file.", action='store_true')
    
    arg = parser.parse_args()
    if arg.synonym is None and arg.recompute and arg.merge:
        print("Nothing to do. Give a word, merge json files or recompute.")
        exit()
    return arg

    


class no_name(object):
    def __init__(self):
        self.data = ""

    def load_file(self, file_in):
        with open(file_in, 'r') as f:
            info = json.load(f)
            return info

    def merge_files(self):
        print("Merging dictionary files into single file.")
        result = []
        for f in glob.glob("*.json"):
            with open(f, "r") as infile:
                print("Current file: %s", f)
                result.append(json.load(infile))

        with open("merged_file.txt", "w") as outfile:
            json.dump(result, outfile)

    def check_options(self, file_in=None):
        if arg_options.merge:
            self.merge_files()
        if arg_options.file is not None:
            self.data = self.load_file(file_in);

    def search_word(self, word_in):
        #print(self.data[word_in])
        word = self.data[word_in]
        print(word["MEANINGS"])
        print(word["ANTONYMS"])
        print(word["SYNONYMS"])

if __name__ == "__main__":
    arg_options = launch_options()
    test = no_name()
    test.check_options(arg_options.file)
    test.search_word(arg_options.synonym.upper()) #dictionary is all uppercase    
     
    #Not always needed, only needed when recomputing the tables
    #processed_data = find_connections(data);
    #Synthetic neural mesh??
    #Do not try to shortcut data path between nodes.
    #Add retry option for computing different synonyms? Pre-computed hastable?
    #syn = input()
    #find_likelyhood(syn)
    #print(highest_vals)
    # Hold computed values in N-dimensional array or hastable

