import string
import random

class BlogWriter():
    '''
    In an amazing attempt at laziness, I am writing a program to write
    my Geeks Who Drink Blogs for me.  Because how Geek is that?
    '''

    def __init__(self, file_name, n_grams=2, num_words=10):
        self.f = open(file_name)
        self.n_gram = n_grams
        self.num_words = num_words

    def letters_only(self, input_string):
        '''
        Returns only letters...and whatever else I set here.
        '''
        good = "abcdefghijklmnopqrstuvwxyz1234567890'.-?!"
        input_string = input_string.lower()
        lst = [a for a in input_string if a in string.ascii_lowercase]
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
        if n_gram >= 2:
            keys = [a[0] for a in dct.keys()]
        else:
            keys = list(dct.keys())
        if n_gram == 1:
            lst = [random.choice(list(dct.keys()))]
        else:
            lst = list(random.choice(list(dct.keys())))
        while len(lst) < self.num_words:
            a = tuple(lst[start:])
            if n_gram == 1:
                a = (a[0])
            b = dct[a]
            c = random.choice(b)
            lst.append(c)
        return ' '.join(lst)
