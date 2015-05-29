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
        self.__code = [
        ["0000", "0001", "0011", "0010"],
        ["0100", "0101", "0111", "0110"],
        ["1100", "1101", "1111", "1110"],
        ["1000", "1001", "1011", "1010"]
        ]
        self.chars = ['a', 'b', 'c', 'd']
        self.input2sequence = [0, 1, 3, 2, 4, 5, 7, 6, 8, 9, 11, 10, 12, 13, 15, 14]

    def solve(self, selected):
        h = len(selected)
        if h != 4: return False
        w = len(selected[0])
        if w != 4: return False

        elements = count_selected(selected, w, h)

        c = len(elements)
        if c == 16: return "1"
        
        if not (c == 1 or c == 2 or c == 4 or c == 8):
            return False
        
        __codes = [self.__code[i/4][i%4] for i in elements]
        
        for i in range(c):
            #code = [[c for c in self.__code[elem]] for elm in elements]
            found = False
            temp = []
            for j in range(len(__codes)-1):
                if found: break
                for k in range(j+1, len(__codes)):
                    m = self.merge(__codes[j], __codes[k])
                    if m != False:
                        
                        found = True
                        __codes[j] = m
                        del __codes[k]
                        break

            if not found: break

        if len(__codes) > 1: return False
        
        return self.to_chars(__codes[0])
        
    def merge(self, s1, s2):
        c = -1
        l = 4
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