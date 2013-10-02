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


def make_chains(corpus):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    list_of_words = corpus.lower().split()
    chain_dict = {}

    for i in range(len(list_of_words)):
        list_of_words[i] = list_of_words[i].strip(';,.!?"\'\n\t()')

    for i in range(len(list_of_words)-2):
        key = (list_of_words[i], list_of_words[i+1])
        value = list_of_words[i+2]
        chain_dict.setdefault(key, []).append(value)

    return chain_dict


def make_text(chains):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    sentence = []
    random_tuple = choice(chains.keys())
    sentence.append(random_tuple[0])
    sentence.append(random_tuple[1])

    for i in range(19):
        key = (sentence[i], sentence[i+1])
        rand_word = choice(chains[key])
        sentence.append(rand_word)

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

    #api.PostUpdate(post)

def main():
    
    script, source = argv

    # Change this to read input_text from a file
    input_text = open_and_read(source)

    chain_dict = make_chains(input_text)
    random_text = make_text(chain_dict)

    pretty_string = " ".join(random_text)
    post_to_twitter(pretty_string)

    for i in random_text:
       print i, 
    

if __name__ == "__main__":
    main()



