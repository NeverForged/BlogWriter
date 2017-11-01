import time
import gensim
import random
import string
import numpy as np


class BlogWriter():
    '''
    In an amazing attempt at laziness, I am writing a program to write
    my Geeks Who Drink Blogs for me.  Because how Geek is that?
    '''

    def __init__(self, file_name, n_grams=2, num_words=10, topic="beer",
                 topic_check=2):
        self.f = open(file_name)
        self.n_gram = n_grams
        self.num_words = num_words
        self.topic = topic
        self.topic_n = topic_check
        self.model = self.get_google()

    def letters_only(self, input_string):
        '''
        Returns only letters...and whatever else I set here.
        '''
        good = "abcdefghijklmnopqrstuvwxyz1234567890'.-?!"
        input_string = input_string.lower()
        lst = [a for a in input_string]
        return ''.join(lst)

    def associated_unigrams(self, f):
        '''
        INPUT: file
        OUTPUT: dictionary

        Return a dictionary where the keys are words in the file inside a tuple
        and the value for each key is a list of words that were found directly
        following the key.

        Words should be included in the list the number of times they appear.

        Suggestions on how to handle first word: create an entry in the dictionary
        with a first key (None)

        Example:
        >>> with open('../data/alice.txt') as f:
        ...     d = associated_unigrams(f)
        >>> d[('among')]
        ['the', 'those', 'them', 'the', 'the', 'the', 'the', 'the', 'the', 'mad', 'the', 'them']
        '''
        text = f.read().split()
        dct = {}
        for n in range(len(text)-1):
            a = self.letters_only(text[n])
            b = self.letters_only(text[n+1])
            try:
                dct[(a)].append(b)
            except:  # failure...
                dct[(a)] = [b]
        return dct

    def associated_bigrams(self, f):
        '''
        INPUT: file
        OUTPUT: dictionary
        '''
        text = f.read().split()
        dct = {}
        for n in range(len(text)-2):
            a = (self.letters_only(text[n]), self.letters_only(text[n+1]))
            b = self.letters_only(text[n+2])
            try:
                dct[(a)].append(b)
            except:  # failure...
                dct[(a)] = [b]
        return dct

    def associated_trigrams(self, f):
        '''
        INPUT: file
        OUTPUT: dictionary

        Return a dictionary where the keys are tuples of three consecutive words in
        the file and the value for each key is a list of words that were found
        directly following the key.

        Words should be included in the list the number of times they appear.
        '''
        text = f.read().split()
        dct = {}
        for n in range(len(text)-3):
            a = (self.letters_only(text[n]),
                 self.letters_only(text[n + 1]),
                 self.letters_only(text[n + 2]))
            b = self.letters_only(text[n + 3])
            try:
                dct[(a)].append(b)
            except:  # failure...
                dct[(a)] = [b]
        return dct

    def get_google(self):
        '''
        Loads google news word2vec model
        '''
        start = time.clock()
        # b = '../model/300features_5min_word_count_10context.npy'
        b = 'model/GoogleNews-vectors-negative300.bin'
        try:
            model = gensim.models.KeyedVectors.load_word2vec_format(b, binary=True)
        except:
            model = gensim.models.Word2Vec.load(b)
        model.init_sims(replace=True)  # save memory
        print("This took only {:.3f}s".format(time.clock()-start))
        return model

    def get_cos_sim(self, word):
        ret = 0
        if self.topic_n == 1:
            ret = (random.randint(0,3) + random.randint(0,3))/7
        else:
            try:
                ret = self.model.wv.similarity(self.topic, word)
            except:
                ret = 0.0
        return ret

    def make_random_story(self):

        '''
        INPUT: file, integer, interger
        OUTPUT: string

        Call associated_n_grams (associated_unigrams, associated_bigrams or
        associated_trigrams for n_gram set at 1, 2 or 3) on file f and use the
        resulting dictionary to randomly generate text with num_words total words.

        Choose the next word by using random.choice to pick a word from the list
        of possibilities given the last two words.

        Use join method to turn a list of words into a string.

        Example:
        >>> # Seed the random number generator for consistent results
        >>> random.seed('Is the looking-glass is half full or half-empty?')
        >>> # Generate a random story
        >>> with open('../data/alice.txt') as f:
        ...     story = make_random_story(f, 2, 10)
        ...     story  # Note: your random story may not match this example
        stick, and tumbled head over heels in its sleep 'twinkle,
        >>> len(story.split())  # Verify story length is 10 words
        10
        '''
        n_gram = self.n_gram
        if n_gram == 1:
            dct = self.associated_unigrams(self.f)
        elif n_gram == 2:
            dct = self.associated_bigrams(self.f)
        else:
            dct = self.associated_trigrams(self.f)
        lst = []
        start = 0 - n_gram

        keys = list(dct.keys())
        print(keys[0])
        if n_gram == 1:
            lst = [random.choice(keys)]
        else:
            lst = list(random.choice(keys))
        print(lst)
        while len(lst) < self.num_words:
            try:
                if n_gram == 1:

                    a_tuple = (lst[-1])
                else:
                    a_tuple = tuple(lst[start:])
                b_lst = dct[a_tuple]
                c_lst = np.random.choice(b_lst, self.topic_n)
                sims = [self.get_cos_sim(a) for a in c_lst]
                lst.append(c_lst[sims.index(max(sims))])
            except:
                lst.append(random.choice(keys))

        # punctuation
        period = True
        endings = '.?!'
        nlst = []
        for word in lst:
            word_lst = list(word)
            if period == True:
                # capitalize it
                word_lst[0] = word_lst[0].upper()
                word = ''.join(word_lst)
                period = False
            if word_lst[-1] in endings:
                period = True
            if word == 'i':
                word.upper()
            nlst.append(word)
        return ' '.join(nlst)
