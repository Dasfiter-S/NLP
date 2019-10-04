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
    def load_file(self, file_in):
        with open(file_in, 'r') as f:
            info = json.loads(f)
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

    def check_options(self):
        if arg_options.merge:
            self.merge_files()
        #if arg_options.file is not None:
        #    json_data = test_item.load_file(file_in);
        #if arg_options.recompute:
        #    json_data = test_item.load_file(default_data);


if __name__ == "__main__":
    arg_options = launch_options()
    test = no_name()
    test.check_options()
    #Not always needed, only needed when recomputing the tables
    #processed_data = find_connections(data);
    #Synthetic neural mesh??
    #Do not try to shortcut data path between nodes.
    #Add retry option for computing different synonyms? Pre-computed hastable?
    #syn = input()
    #find_likelyhood(syn)
    #print(highest_vals)
    # Hold computed values in N-dimensional array or hastable

