from peace import *
from helper import *

class Action:
    '''
    Undoable action
    '''
    def __init__(self, context=None, action_number=0):
        self.context = context
        self.action_number = action_number
        self.done = False
        self.undone = False

    def set_params(self, *args, **kwargs):
        pass

    def do(self):
        pass

    def undo(self):
        pass

class SelectAction(Action):
    '''
    select a box
    '''

    def set_params(self, w, h):
        self.w = w
        self.h = h

    def do(self):
        w = self.w
        h = self.h
        self.v = self.context.selected_buttons[self.h][self.w]
        self.bg = self.context.map_buttons[h][w]['bg']

        if self.context.selected_buttons[self.h][self.w] == 0:
            self.context.selected_buttons[h][w] = 1
        else: self.context.selected_buttons[h][w] = 0
        if self.context.selected_buttons[h][w] == 0:
            self.context.map_buttons[h][w].config(bg="#ffc000")
        else:
            self.context.map_buttons[h][w].config(bg="#c0ff00")

        self.done = True

    def undo(self):
        if self.context.action_count == self.action_number + 1:

            self.context.selected_buttons[self.h][self.w] = self.v
            self.context.map_buttons[self.h][self.w]['bg'] = self.bg
        else:
            pprint("Error: action mismatch")

class FlipAction(Action):
    '''
    flip a set of box
    '''

    def do(self):
        self.values = []
        solution = self.context.algo.solve(self.context.selected_buttons)
        print solution
        if(solution == False):
            self.done = False
            return

        self.output_value = self.context.output.get()
        found = False
        for h in range(self.context.map_h):
            for w in range(self.context.map_w):
                if self.context.selected_buttons[h][w] == 0: continue

                found = True
                self.values.append((w,h, self.context.values_of_buttons[h][w]))
                if self.context.values_of_buttons[h][w] == 0:
                    self.context.values_of_buttons[h][w] = 1
                elif self.context.values_of_buttons[h][w]  == 1:
                    self.context.values_of_buttons[h][w] = 0
                else: #case of don't care
                    self.context.values_of_buttons[h][w] = 3
                self.context.map_buttons[h][w]['text'] = int_to_char_to_display(self.context.values_of_buttons[h][w])

                self.context.selected_buttons[h][w] = 0
                self.context.map_buttons[h][w].config(bg="#ffc000")

        if not found: return
        if self.output_value == "":
            tk_entry_text(self.context.output, solution)
        else: tk_entry_text(self.context.output, self.output_value + " ^ " + solution)
        self.done = True

    def undo(self):
        if self.context.action_count != self.action_number + 1:
            return
        for i in range(len(self.values)):
            v = self.values[i]
            self.context.values_of_buttons[v[1]][v[0]] = v[2]
            self.context.map_buttons[v[1]][v[0]]['text'] = int_to_char_to_display(int(v[2]))
            self.context.selected_buttons[v[1]][v[0]] = 1
            self.context.map_buttons[v[1]][v[0]].config(bg="#c0ff00")

        tk_entry_text(self.context.output, (self.output_value))
