#import tensorflow as tf
import argparse

#commandline options
def launch_options():
    parser = argparse.ArgumentParser("This program analyzes synonyms and returns the most\
                                  likely candidates that are similar to the word provided.")
    parser.add_argument('-s', '--synonym', help='Choose a word to analyze')
    parser.add_argument('-f', '--file', help='')


class no_name(object):

    def load_file(file_in):
        with open(file_in, 'r') as loaded_file:
           info = loaded_file.readlines()
           return info


if __name__ == "__main__":
    test_item = no_name()
    #data = test_item.load_file(file_in);

    #Not always needed, only needed when recomputing the tables
    #processed_data = find_connections(data);
    #Synthetic neural mesh??
    #Do not try to shortcut data path between nodes.
    #syn = input()
    #find_likelyhood(syn)
    #print(highest_vals)

