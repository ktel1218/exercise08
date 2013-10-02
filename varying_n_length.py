   #!/usr/bin/env python
# make list of tuples

from sys import argv
from random import choice
import twitter


def open_and_read(filename):
    f = open(filename)
    file_text = f.read()
    f.close
    return file_text

def make_key(word_list, looping_index, n_gram_length):
    """takes a word list and a looping value and makes a key for the dictionary"""
    list_for_key = []

    for n in range(n_gram_length):
        list_for_key.append(word_list[looping_index+n])
    
    key = tuple(list_for_key)
    return key

def make_chains(corpus, n_length):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    list_of_words = corpus.lower().split()
    chain_dict = {}

    # stripping punctuation from words
    for i in range(len(list_of_words)):
        list_of_words[i] = list_of_words[i].strip(';,.!?"\'\n\t()')

   # entering each key: value pair into the dictionary
    for i in range(len(list_of_words)-n_length):
        key = make_key(list_of_words, i, n_length)
        value = list_of_words[i+n_length]
        # check if the key is in a dictionary
            # if the key does not exist, set the value to an empty list
            # if the key does exist, append the word to the list
        chain_dict.setdefault(key, []).append(value)

    return chain_dict

def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    # pick first n words to start chain
    random_tuple = choice(chains.keys())
    sentence = list(random_tuple)

    #fill in the rest of the sentence chain
    for i in range(21-len(random_tuple)):
        key = make_key(sentence, i, len(random_tuple))
        rand_word = choice(chains[key])
        sentence.append(rand_word)

    # formatting
    for i in range(len(sentence)):
        if i % 7 == 0:#first word on the line
            sentence[i] = sentence[i].capitalize()
        if i == (len(sentence)-1):#last word in the stanza
            sentence[i] += "."
        elif i % 7 == 6: #last word on the line
            sentence[i] += ",\n"

    return sentence

def post_to_twitter(post):    
    consumer_key = "zRRzFlKoWUW3KWAY2rfSA"
    consumer_secret = "qIlmOKGuTs6A304Kh4hpjZn6XGh3yHqKManyY8V2TY"
    access_token_key = "1925040590-QBQBryQXhIyVOmxl4J0W8hB6TVVEZ9IwZflmqCO"
    access_token_secret = "pSqfZ9XfKJWcu74DFOyib3zUedQNfEBMpPSulWa7M"


    api = twitter.Api(consumer_key,
                    consumer_secret,
                    access_token_key,
                    access_token_secret)

    api.PostUpdate(post)

def main():
    
    script, source = argv

    n_length = int(raw_input("length of n-gram?> "))

    # Change this to read input_text from a file
    input_text = open_and_read(source)

    chain_dict = make_chains(input_text, n_length)
    random_text = make_text(chain_dict)

    pretty_string = " ".join(random_text)
    post_to_twitter(pretty_string)

    for i in random_text:
       print i, 
    

if __name__ == "__main__":
    main()