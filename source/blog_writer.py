import time
import gensim
import random
import string
import pickle
import numpy as np
from nltk import pos_tag, word_tokenize


class BlogWriter():
    '''
    In an amazing attempt at laziness, I am writing a program to write
    my Geeks Who Drink Blogs for me.  Because how Geek is that?
    '''

    def __init__(self, file_name, n_grams=2, num_words=10, topic="beer",
                 topic_check=2, model=None, verbose=False):
        self.f = open(file_name)
        self.n_gram = n_grams
        self.num_words = num_words
        self.topic = topic
        self.topic_n = topic_check
        d_name = 'data/basic_english.pickle'
        with open(d_name, 'rb') as f:
            self.class_dictionary = pickle.load(f, encoding='UTF-8')
        self.verbose = verbose
        if model == None:
            self.model = self.get_google()

    def letters_only(self, input_string):
        '''
        Returns only letters...and whatever else I set here.
        '''
        good = "abcdefghijklmnopqrstuvwxyz1234567890'.-?!"
        input_string = input_string.lower()
        lst = [a for a in input_string]
        return ''.join(lst)

    def replace_punctuation(self, input_text):
        '''
        breaks up punctuation to avoid it.
        '''
        txt = input_text.replace('...', ' ...').replace('.',' .')
        txt = txt.replace('. . .','...')
        txt = txt.replace('?',' ?').replace('!',' !')
        txt = txt.replace('(','( ').replace(')',' )')
        txt = txt.replace('"',' " ')
        txt = txt.replace('-', ' - ')
        return txt

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
        ['the', 'those', 'them', 'the', 'the', 'the', 'the']
        '''
        text = f.read()
        text = self.replace_punctuation(text)
        text = text.split()
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
        text = f.read()
        text = self.replace_punctuation(text)
        text = text.split()
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
        text = f.read()
        text = self.replace_punctuation(text)
        text = text.split()
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


    def check_replace(self, tag):
        pass_thru = ['CD',  # CD: numeral, cardinal
                     'EX',  # EX: existential there
                     'FW',  # FW: foreign word
                     'LS',  # LS: list item marker
                     'JJ',  # JJ: adjective or numeral, ordinal
                     'NNP',  # NNP: noun, proper, singular
                     'NNPS',  # NNPS: noun, proper, plural
                     'PRP',  # PRP: pronoun, personal
                     'SYM',  # SYM: symbol
                     'TO',  # TO: "to" as preposition or infinitive marker
                     'POS',
                     '$',  # $: dollar
                     '(',
                     ')',
                     ',',
                     '.',
                     ':',
                     '"'
                     ]
        if tag in pass_thru:
            return True
        else:
            return False

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
        return lst

    def basic_english_fit(self, input_text):
        '''
        (from BasicEnglishTranslator)
        The actual translation occurs here:
        Methodology:
            Takes an input text, turns it to a list w/parts of speach tagging,
            then based on the part of speach, replaces certain words with
            Basic English words from the dictionary.
        Input: String
        '''
        print('start',input_text)
        # timer...
        start = time.clock()
        # printable filter
        prt = set(string.printable)
        input_text = input_text #filter(lambda x: x in prt, input_text)
        # save input text
        self.real_text = input_text
        # add to sentences for next time we rebuild our model...
        print('input_text:',input_text)
        words = pos_tag(input_text.split(' '))  # makes a list of words...
        print('words', words)
        self.real_list = words
        # These simply pass thru the model
        pass_thru = ['CD',  # CD: numeral, cardinal
                     'EX',  # EX: existential there
                     'FW',  # FW: foreign word
                     'LS',  # LS: list item marker
                     'JJ',  # JJ: adjective or numeral, ordinal
                     'NNP',  # NNP: noun, proper, singular
                     'NNPS',  # NNPS: noun, proper, plural
                     'PRP',  # PRP: pronoun, personal
                     'SYM',  # SYM: symbol
                     'TO',  # TO: "to" as preposition or infinitive marker
                     'POS',
                     '$',  # $: dollar
                     '(',
                     ')',
                     ',',
                     '.',
                     ':',
                     '"'
                     ]
        # make these Basic
        make_simple = ['CC',  # CC: conjunction, coordinating
                       'DT',  # DT: determiner
                       'IN',  # IN: preposition or conjunction, subordinating
                       'JJR',  # JJR: adjective, comparative
                       'JJS',  # JJR: adjective, comparative
                       'MD',  # MD: modal auxiliary
                       'NN',  # NN: noun, common, singular or mass
                       'NNS',  # NNS: noun, common, plural
                       'PDT',  # PDT: pre-determiner
                       'PDT',  # PDT: pre-determiner
                       'PRP$',  # PRP$: pronoun, possessive
                       'RB',  # RB: adverb
                       'RBR',  # RBR: adverb, comparative
                       'RBS',  # RBS: adverb, superlative
                       'RP',  # RP: particle
                       'UH',  # UH: interjection
                       'VB',  # VB: verb, base form
                       'VBD',  # VBD: verb, past tense
                       'VBG',  # VBG: verb, present participle or gerund
                       'VBN',  # VBN: verb, past participle
                       'VBP',  # VBP: verb, present tense, not 3rd person sing
                       'VBZ',  # VBZ: verb, present tense, 3rd person singular
                       'WDT',  # WDT: WH-determiner
                       'WP',  # WP: WH-pronoun
                       'WP$',  # WP$: WH-pronoun, possessive
                       'WRB'  # WRB: Wh-adverb
                       ]
        count_replacements = 0
        self.lst_ret = []
        for idx, word in enumerate(words):
            if word[1] in pass_thru or len(word[0]) <= 1:
                # put it in and move on... it's proper or whatever
                self.lst_ret.append(word[0])
            else:
                # We have a word we need to replace...
                # bath it...
                clean = word[0].strip(string.punctuation).lower()
                # ...and bring it to the function
                # already simple... throw it in and move on
                if clean in self.class_dictionary:
                    temp = self.class_dictionary[clean][0]
                    if pos_tag([temp])[0][1] == word[1]:
                        self.lst_ret.append(self.retain_capitalization(temp,
                                                                   word[0]))
                    else:
                        self.lst_ret.append(word[0])
                else:
                    self.lst_ret.append(word[0])
        end = time.clock()
        if self.verbose:
            print('Time: {:.4f}s'.format(end - start))
        print('lst_ret',self.lst_ret)
        txt = ' '.join(self.lst_ret)
        #txt = self.replace_punctuation(' '.join(self.lst_ret))
        #txt = txt.encode('utf-8')
        #txt = re.sub("\xe2\x80\x93", "-", txt)
        self.basic_list = self.lst_ret
        self.basic_text = txt
        print('end', txt)
        return txt

    def rewrite_text(self, lst):
        txt = ' '.join(lst)
        new_lst = self.basic_english_fit(txt).split()
        return new_lst

    def retain_capitalization(self, new_word, original_word):
        '''
        Checks the original_word for capitalization, if it has it, capitalizes
        the frst letter of new_word, returns new_word.
        '''
        if original_word[0] in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            lst = list(new_word)
            lst[0] = lst[0].upper()
            new_word = ''.join(lst)
        return new_word

    def write(self):
        lst =  self.make_random_story()
        return self.rewrite_text(lst)
