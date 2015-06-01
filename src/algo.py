def count_selected(selected, w, h):
    ssss = []
    count = 0
    for i in range(h):
        for j in range(w):
            if selected[i][j] == 1:
                ssss.append(count)
            count = count + 1
    return ssss

class KM4:
    '''
    Karnaugh Map of 4
    '''
    def __init__(self):
        self.special_code = [
        ["0000", "0001", "0011", "0010"],
        ["0100", "0101", "0111", "0110"],
        ["1100", "1101", "1111", "1110"],
        ["1000", "1001", "1011", "1010"]
        ]
        self.chars = ['a', 'b', 'c', 'd']
        self.input2sequence = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]
        #self.input2sequence = [0, 1, 3, 2, 4, 5, 7, 6, 8, 9, 11, 10 , 12, 13, 15, 14]
        self.NE = 4 #number of types - chars' length
        self.W = 4  #width
        self.H = 4  #height
        self.L = 16 #number of inputs

    def solve(self, selected):
        h = len(selected)
        if h != self.H: return False
        w = len(selected[0])
        if w != self.W: return False

        elements = count_selected(selected, w, h)

        c = len(elements)
        if c == self.L: return "1"
        
        if not (c == 1 or c == 2 or c == 4 or c == 8):
            return False
        
        special_codes = [self.special_code[i/self.W][i%self.W] for i in elements]
        print elements, special_codes
        
        for i in range(c):
            #code = [[c for c in self.special_code[elem]] for elm in elements]
            found = False
            temp = []
            for j in range(len(special_codes)-1):
                if found: break
                for k in range(j+1, len(special_codes)):
                    m = self.merge(special_codes[j], special_codes[k])
                    if m != False:
                        
                        found = True
                        special_codes[j] = m
                        del special_codes[k]
                        break

            if not found: break

        if len(special_codes) > 1: return False
        
        return self.to_chars(special_codes[0])
        
    def merge(self, s1, s2):
        c = -1
        l = self.NE
        for i in range(l):
            if s1[i] != s2[i]:
                if c > -1:
                    return False
                c = i

        if c == -1: return s1
        s = ""
        for i in range(l):
            if i == c:
                s = s + '2'
            else:
                s = s + s1[i]
        return s

    def to_chars(self, code):
        s = ""
        for i in range(len(code)):
            if code[i] == '0':
                s = s + self.chars[i] + "'"
            elif code[i] == '1':
                s = s + self.chars[i] 

        return s

    def input2mapsequence(self, map_input):
        sequence = [None] * len(map_input)
        for i in range (len (map_input)):
            if map_input[i] == '0':
                sequence[self.input2sequence[i]] = '0'
            elif map_input[i] == '1':
                sequence[self.input2sequence[i]] = '1'
            else:
                sequence[self.input2sequence[i]] = '3' #don't care characters

        return ''.join(sequence)

    def mapsequence2input(self, map_sequence):
        pass

class KM5(KM4):
    '''
    Karnaugh Map of 5
    '''
    def __init__(self):
        self.special_code = [
        ["00000", "00001", "00011", "00010"],
        ["00100", "00101", "00111", "00110"],
        ["01100", "01101", "01111", "01110"],
        ["01000", "01001", "01011", "01010"],
        ["10000", "10001", "10011", "10010"],
        ["10100", "10101", "10111", "10110"],
        ["11100", "11101", "11111", "11110"],
        ["11000", "11001", "11011", "11010"]    
        ]
        self.chars = ['a', 'b', 'c', 'd', 'e']
        self.input2sequence = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10,\
                               16, 17, 19, 18, 20, 21, 23, 22, 28, 29, 31, 30, 24, 25, 27, 26]
        self.NE = 5 #number of types - chars' length
        self.W = 4  #width
        self.H = 8  #height
        self.L = 32 #number of inputs
