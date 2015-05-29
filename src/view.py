import Tkinter as tk
import ttk
import config
from peace import *
from algo import *
from action import *
from helper import *

class KMapView(tk.Frame):
    '''
    The application view
    '''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="#5b9bd5")

        self.parent = parent
        self.state = 'START'
        self.map_buttons = None
        self.selected_buttons = None
        self.algo = None
        self.action_count = 0
        self.actions = []
        self.map_w = 0
        self.map_h = 0

        self.initUI()
        self.centerWindow()

    def initParams(self):
        self.map_buttons = None
        self.map_input = None
        self.selected_buttons = None
        self.algo = None
        self.action_count = 0
        self.actions = []
        self.map_w = 0
        self.map_h = 0

    def reset(self):
        self.initParams()
        self.select_boxes_button.config(state='disabled')
        self.undo_button.config(state='disabled')
        self.flip_bits_button.config(state='disabled')
        tk_entry_text(self.output, "")

    def initUI(self):
        self.parent.title = "Karnaugh Map Editor"

        self.style = ttk.Style()
        self.style.theme_use("default")

        #select boxes button
        self.select_boxes_button = tk.Button(self,text="Select minterms",command=self.select_boxes,bg="#ffc000")
        self.select_boxes_button.grid(row = 4, column = 2, sticky = 'S')
        self.select_boxes_button.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1), y=config.SPACE_1)
        self.select_boxes_button.config(state='disabled')

        #flip bits button
        self.flip_bits_button = tk.Button(self,text="Map minterms",command=self.flip_bits,bg="#ffc000")
        self.flip_bits_button.grid(row = 4, column = 2, sticky = 'S')
        self.flip_bits_button.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1), y=50 + config.SPACE_1)
        self.flip_bits_button.config(state='disabled')

        #display output button
        self.display_output_button = tk.Button(self,text="Display output with",command=self.foo,bg="#ffc000")
        self.display_output_button.grid(row = 4, column = 2, sticky = 'S')
        self.display_output_button.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1), y=100 + config.SPACE_1)
        self.display_output_button.config(state='disabled')

        #output to a file
        self.file_output_button = tk.Button(self,text="Ouput to a file",command=self.file_output,bg="#ffc000")
        self.file_output_button.grid(row = 4, column = 2, sticky = 'S')
        self.file_output_button.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1 + 150), y=100 + config.SPACE_1)
        self.file_output_button.config(state='disabled')

        #Undo
        self.undo_button = tk.Button(self,text="Undo",command=self.undo,bg="#ffc000")
        self.undo_button.grid(row = 4, column = 2, sticky = 'S')
        self.undo_button.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1 + 100), y=config.SPACE_1)
        self.undo_button.config(state='disabled')

        #Insert Input
        self.insert_button = tk.Button(self,text="Insert Input(4-7 map)",command=self.insert_map,bg="#ffc000")
        self.insert_button.grid(row = 4, column = 2, sticky = 'S')
        self.insert_button.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1-200), y=config.SPACE_1)

        #Insert input
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, columnspan=4, sticky=tk.W+tk.E)
        self.entry.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1-200), y=50+config.SPACE_1)

        #output
        self.output = tk.Entry(self, state="readonly")
        self.output.grid(row=0, columnspan=4, sticky=tk.W+tk.E)
        self.output.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1-200), y=100+config.SPACE_1)

        #output
        self.label = tk.Label(self, text='Output:')
        self.label.grid(row=0, columnspan=4, sticky=tk.W+tk.E)
        self.label.place(x=(config.INITIAL_WIDTH/2 + config.SPACE_1-250), y=100+config.SPACE_1)

        self.pack(fill=tk.BOTH, expand=1)


    def select_boxes(self):
      
        pprint('select_boxes')
        if(self.map_buttons != None):
            for h in range(len(self.map_buttons)):
                for w in range(len(self.map_buttons[h])):
                    self.map_buttons[h][w].config(state='normal')

        else:
            return

        self.state = 'SELECTING'
        self.flip_bits_button.config(state='normal')
        self.select_boxes_button.config(state='disabled')

    def file_output(self):
        f = open(config.OUTPUT_FILE, "w")
        f.write(str(self.map_input) + "\n" )
        f.write(self.output.get() + "\n")
        f.close()

    def undo(self):
        if(self.actions is not None and len(self.actions)>0):
            a = self.actions[-1]
            del self.actions[-1]
            a.undo()
            self.action_count = self.action_count - 1

            if self.action_count == 0:
                self.undo_button.config(state='disabled')

    def flip_bits(self):
        if self.map_buttons != None and self.selected_buttons!= None:
            f = FlipAction(self, self.action_count)
            f.set_params()
            f.do()

            if(f.done):
                self.actions.append(f)
                self.action_count = self.action_count + 1
            else:
                pprint("Error: not done.")

    def insert_map(self):

        self.reset()

        self.map_input = self.entry.get().strip()
        if(self.validate_map_input(self.map_input)):
            self.create_map()
            self.select_boxes_button.config(state='normal')
        else:
            pprint("Error: Invalid Input", self.map_input)

    def validate_map_input(self, txt):
        map_input_array = "".join(txt.split())

        for t in map_input_array:
            if not (t == '0' or t == '1' or t == 'x'):
                return False

        l = len(map_input_array)
        if not (l == 16 or l == 32 or l == 64 or l==128):
            return False

        self.map_input_array = map_input_array
        return True

    def create_map(self):
        '''
        map_input_array will have the form: 
        0000 1110 1111 0000
        '''

        l = len(self.map_input_array)
        if l == 16:
            self.algo = KM4()
            self.create_map_buttons(4,4)
        elif l == 32:
            #TODO
            #pprint("TODO")
            self.create_map_buttons(8,4)
        elif l == 64:
            pprint("TODO")
        elif l == 128:
            pprint("TODO")
        else:
            pprint("Error.")

    def create_map_buttons(self, w, h):

        self.map_input_array = self.algo.input2mapsequence(self.map_input_array)

        if(self.map_buttons is not None):
            for i in range(len(self.map_buttons)):
                for j in range(len(self.map_buttons[i])):
                    self.map_buttons[i][j].destroy()
        self.map_buttons = None

        self.map_w = w
        self.map_h = h

        self.selected_buttons = [[0] * self.map_w for i in range(self.map_h)]
        self.values_of_buttons = [[0] * self.map_w for i in range(self.map_h)]

        top = config.MAP_TOP
        left = config.MAP_LEFT
        self.map_buttons = []
        for j in range(h):
            row_buttons = []
            for i in range(w):
                t = self.map_input_array[j*w + i]
                self.values_of_buttons[j][i] = special_char_to_int(t)
                f = lambda w=i,h=j:self.map_button_clicked(w,h)
                b = tk.Button(self, text = int_to_char_to_display(int(t)), command = f, bg="#ffc000", state='disabled') 
                b.grid(row=1, column=1)
                b.config(width=6, height=3)
                b.place(x=(left + config.MAP_BUTTON_W * i), y=(top + config.MAP_BUTTON_H*j))

                row_buttons.append(b)
            self.map_buttons.append(row_buttons)


        self.display_output_button.config(state='normal')
        self.file_output_button.config(state='normal')

    def map_button_clicked(self, w, h):
        pprint("map_button_clicked", w, h)
        if self.state != "SELECTING":
            return
        if (self.map_buttons != None and self.selected_buttons != None):
            s = SelectAction(self, self.action_count)
            s.set_params(w, h)
            s.do()
            if s.done:
                self.actions.append(s)
                self.action_count = self.action_count + 1
                self.undo_button.config(state='normal')


    def centerWindow(self):
        '''
        centralize the window
        '''
        w = config.INITIAL_WIDTH
        h = config.INITIAL_HEIGHT

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def foo(self):
        pprint("FOOOOOOOOOOOOOOOOOOOOOOOO.")


