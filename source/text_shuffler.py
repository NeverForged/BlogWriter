import random

class ShuffleText():
    '''
    Shuffles text files to make a larger file... to stagger begining/ending
    things (more variance between different ideas)
    '''

    def __init__(self, file_name, shuffles=5):
        self.file_name = file_name
        self.shuffles = shuffles

    def shuffle(self, output):
        paragraph = ''
        lst = []
        with open(self.file_name) as f:
            for line in f.readlines():
                if len(line) >= 2:
                    lst.append(line)
                else:
                    lst.append('-break-')
        new = ''
        print(len(lst))
        for i in range(self.shuffles):
            random.shuffle(lst)
            new = new + ' '.join(lst)
        new.replace(' /n ','-break-').replace('/n','-break-')

        with open(output, 'w') as f:
            f.write(new)
