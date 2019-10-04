import tensorflow as tf
import argparse
import glob
import json

#from __future__ import absolute_import, division, print_function, unicode_literals

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

    
class Trainer(object):
    def __init__(self):
        self.weight = tf.Variable(5.0)
        self.bias = tf.Variable(0.0)

    def __call__(self, x):
            return self.weight * x + self.bias

        #model = Trainer()
        #assert model(3.0).numpy() == 15.0

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
    #test.check_options(arg_options.file)
    #test.search_word(arg_options.synonym.upper()) #dictionary is all uppercase    
    #______________________TF TEST

    def loss(predicted_y, target_y):
          return tf.reduce_mean(tf.square(predicted_y - target_y))
    TRUE_W = 3.0
    TRUE_b = 2.0
    NUM_EXAMPLES = 1000

    inputs  = tf.random.normal(shape=[NUM_EXAMPLES])
    noise   = tf.random.normal(shape=[NUM_EXAMPLES])
    outputs = inputs * TRUE_W + TRUE_b + noise
    def train(model, inputs, outputs, learning_rate):
        with tf.GradientTape() as t:
            current_loss = loss(model(inputs), outputs)
        dW, db = t.gradient(current_loss, [model.weight, model.bias])
        model.weight.assign_sub(learning_rate * dW)
        model.bias.assign_sub(learning_rate * db)

    model = Trainer()
    Ws, bs = [], []
    epochs = range(10)
    for epoch in epochs:
        Ws.append(model.weight.numpy())
        bs.append(model.bias.numpy())
        current_loss = loss(model(inputs), outputs)

        train(model, inputs, outputs, learning_rate=0.1)
        print('Epoch %2d: W=%1.2f b=%1.2f, loss=%2.5f' %
             (epoch, Ws[-1], bs[-1], current_loss))
    #________________________
    #Not always needed, only needed when recomputing the tables
    #processed_data = find_connections(data);
    #Synthetic neural mesh??
    #Do not try to shortcut data path between nodes.
    #Add retry option for computing different synonyms? Pre-computed hastable?
    #syn = input()
    #find_likelyhood(syn)
    #print(highest_vals)
    # Hold computed values in N-dimensional array or hastable

