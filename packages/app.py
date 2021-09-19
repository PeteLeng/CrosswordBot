# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 19:44:54 2021

@author: Pete
"""
from word import *
from crossword import *
from fitter import *
from plotter import *
from sorter import *
import subprocess
import os
import io
from PIL import EpsImagePlugin
import tkinter as tk

class App(tk.Tk):
    def __init__(self, title='The Crossword Bot!'):
        super().__init__()
        self.title(title)
        self.create_frames()
        self.create_widgets()
        self.display_size = 14
        self.preview = 0
        self.words = []
        self.crosswords = []
        self.pointer = 0
        self.gen = None
        self.cnv_out.draw_squares(self.display_size)
        self.bind_functions()
    
    def create_frames(self):
        self.frm_in = tk.Frame(self)
        self.frm_out = tk.Frame(self)
        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.frm_in.grid(row=0, column=0, sticky='ns')
        self.frm_out.grid(row=0, column=1, sticky='nsew')
        
        # Input subframe
        self.frm_in_title = tk.Frame(self.frm_in)
        self.frm_in_control = tk.Frame(self.frm_in)
        # Layout
        self.frm_in.rowconfigure(0, minsize=30)
        self.frm_in.rowconfigure(1, weight=1)
        # self.frm_in.columnconfigure(0, weight=1)
        self.frm_in_title.grid(row=0, column=0, sticky='nsew')
        self.frm_in_control.grid(row=1, column=0, sticky='nsew')
        
        # Output subframe
        self.frm_out_control = tk.Frame(self.frm_out, bg='light steel blue')
        self.frm_out_display = tk.Frame(self.frm_out)
        # Layout
        # self.frm_out.rowconfigure(0)
        self.frm_out.rowconfigure(1, weight=1)
        self.frm_out.columnconfigure(0, weight=1)
        self.frm_out_control.grid(row=0, column=0, stick='ew')
        self.frm_out_display.grid(row=1, column=0, sticky='nsew')
        
    def create_widgets(self):
        # Input widgets
        self.lbl_in = tk.Label(self.frm_in_title, text='Input your words below!', bg='light steel blue', relief=tk.RAISED, font=('Times', 12), anchor=tk.W)
        self.lbl_txt = tk.Label(self.frm_in_control, text='Enter each word a line:', font=('Times', 12), anchor=tk.W, bg='white smoke')
        self.txt_in = tk.Text(self.frm_in_control, width=30, font=('Times, 12'))
        # self.txt_in.insert('1.0', 'Enter the words in all CAPS,\neach word a line:\n')
        self.btn_in_assemble = tk.Button(self.frm_in_control, text='Assemble the words!')
        self.btn_in_clear = tk.Button(self.frm_in_control, text='Clear the words!')
        # Layout
        self.frm_in_title.rowconfigure(0, weight=1)
        self.frm_in_title.columnconfigure(0, weight=1)
        self.lbl_in.grid(row=0, column=0, sticky='nsew')
        self.frm_in_control.rowconfigure(1, weight=1)
        self.lbl_txt.grid(row=0, column=0, sticky='ew')
        self.txt_in.grid(row=1, column=0, sticky='nsew')
        self.btn_in_assemble.grid(row=2, column=0, sticky='ew')
        self.btn_in_clear.grid(row=3, column=0, sticky='ew')
        
        # Output widgets
        self.btn_out_minus = tk.Button(self.frm_out_control, text='-')
        self.btn_out_plus = tk.Button(self.frm_out_control, text='+')
        self.btn_out_prev = tk.Button(self.frm_out_control, text='PREV')
        self.btn_out_next = tk.Button(self.frm_out_control, text='NEXT')
        self.btn_out_view = tk.Button(self.frm_out_control, text='VIEW')
        self.btn_out_save = tk.Button(self.frm_out_control, text='SAVE')
        self.cnv_out = Grid(self.frm_out_display, bg='white smoke')
        # Layout
        self.frm_out_control.columnconfigure(0, minsize=45)
        self.frm_out_control.columnconfigure(1, minsize=45)
        self.frm_out_control.columnconfigure(2, minsize=45)
        self.frm_out_control.columnconfigure(3, minsize=45)
        self.frm_out_control.columnconfigure(4, minsize=45)
        self.frm_out_control.columnconfigure(5, minsize=45)
        self.btn_out_minus.grid(row=0, column=0, sticky='ew')
        self.btn_out_plus.grid(row=0, column=1, sticky='ew')
        self.btn_out_prev.grid(row=0, column=2, sticky='ew')
        self.btn_out_next.grid(row=0, column=3, sticky='ew')
        self.btn_out_view.grid(row=0, column=4, sticky='ew')
        self.btn_out_save.grid(row=0, column=5, sticky='ew')
        self.frm_out_display.rowconfigure(0, weight=1)
        self.frm_out_display.columnconfigure(0, weight=1)
        self.cnv_out.grid(row=0, column=0, sticky='nsew')
        
    def assemble_words(self, event):
        text = self.txt_in.get('1.0', tk.END)
        split_text = [w.strip(',').upper() for w in text.split('\n') if w]
        length = len(split_text)
        freq_shuffle(split_text, 0, length-1, int((length-1)/2))
        if split_text and split_text != self.words:
            self.words = split_text
            self.gen = genCrosswords(self.words)
            self.crosswords = []
            self.pointer = 0
            try:
                self.crosswords.append(next(self.gen))
                self.plot_crossword()
            except StopIteration:
                print('No crossword available!')
                self.cnv_out.clear_fills()
        
    def clear_words(self, event):
        self.txt_in.delete('1.0', tk.END)
        # self.txt_in.insert('3.0', '\n')
        
    def next_crossword(self, event):
        if self.preview:
            print('Stop preview mode first!')
            return
        if self.crosswords:
            if self.pointer < len(self.crosswords)-1:
                self.pointer += 1
            else:
                try:
                    self.crosswords.append(next(self.gen))
                    self.pointer += 1
                except StopIteration:
                    print('This is the last crossword!')
            self.plot_crossword()
        else:
            print('Assemble words before hitting NEXT')
    
    def prev_crossword(self, event):
        if self.preview:
            print('Stop preview mode first!')
            return
        if self.crosswords:
            if self.pointer > 0:
                self.pointer -= 1
                self.plot_crossword()
            else:
                print('This is the first crossword!')
        else:
            print('Assemble words before hitting PREV')
    
    def increase_size(self, event):
        if self.preview:
            print('Stop preview mode first!')
            return
        self.display_size += 1
        self.cnv_out.clear_squares()
        self.cnv_out.draw_squares(self.display_size)
        if self.crosswords:
            self.plot_crossword()
    
    def decrease_size(self, event):
        if self.preview:
            print('Stop preview mode first!')
            return
        self.display_size -= 1
        self.cnv_out.clear_squares()
        self.cnv_out.draw_squares(self.display_size)
        if self.crosswords:
            self.plot_crossword()
            
    def preview_crossword(self, event):
        self.preview = 1 - self.preview
        cw = plot(self.crosswords[self.pointer], self.display_size)
        if self.preview:
            self.cnv_out.clear_fills()
            self.cnv_out.clear_squares()
            self.cnv_out.draw_squares(self.display_size, 'preview')
            self.cnv_out.preview_squares(cw)
        else:
            self.cnv_out.clear_fills()
            self.cnv_out.clear_squares()
            self.cnv_out.draw_squares(self.display_size, 'default')
            self.cnv_out.fill_squares(cw)
    
    def save_crossword(self, event):
        if self.preview:
            height = self.display_size*self.cnv_out.square_size
            width = self.display_size*self.cnv_out.square_size
            x = self.cnv_out.x_pad*self.cnv_out.square_size
            y = self.cnv_out.y_pad*self.cnv_out.square_size
            self.cnv_out.postscript(file="C:\\Pete\\Project\\Crossword\\result\\result.ps", colormode="color", height=height, width=width, x=x, y=y)
            
            # Convert to image using ghostscript, didn't resolve resolution problem
            # EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs9.54.0\bin\gswin64c'
            # img = Image.open(io.BytesIO(ps.encode('utf-8')))
            # # print(img)
            # img.save('crossword.png')
            
            # Convert to pdf using subprocess, didn't work
            # process = subprocess.Popen(["ps2pdf", "tmp.ps", "result.pdf"], shell=True)
            # process.wait()
            # os.remove("tmp.ps")
            
    def bind_functions(self):
        self.btn_in_assemble.bind('<Button-1>', self.assemble_words)
        self.btn_in_clear.bind('<Button-1>', self.clear_words)
        self.btn_out_next.bind('<Button-1>', self.next_crossword)
        self.btn_out_prev.bind('<Button-1>', self.prev_crossword)
        self.btn_out_minus.bind('<Button-1>', self.decrease_size)
        self.btn_out_plus.bind('<Button-1>', self.increase_size)
        self.btn_out_view.bind('<Button-1>', self.preview_crossword)
        self.btn_out_save.bind('<Button-1>', self.save_crossword)
    
    def plot_crossword(self):
        self.preview = 0
        self.cnv_out.clear_fills()
        cw = plot(self.crosswords[self.pointer], self.display_size)
        self.cnv_out.fill_squares(cw)

class Grid(tk.Canvas):
    def __init__(self, parent, **kws):
        super().__init__(parent, **kws)
        self.squares = {}
        self.config = {'preview':{'fill':'snow', 'outline':'snow3'},
                       'default':{'fill':'white smoke', 'outline':'black'}}
        # self.fills = {}
        self.square_size = 40
        self.x_pad = 1.5
        self.y_pad = 1.5

    def draw_squares(self, display_size, mode='default'):
        config = self.config[mode]
        x_start, y_start = self.x_pad*self.square_size, self.y_pad*self.square_size
        square_size = self.square_size
        for i in range(display_size):
            for j in range(display_size):
                self.squares[(i, j)] = self.create_rectangle(x_start+i*square_size, y_start+j*square_size, 
                                                             x_start+(i+1)*square_size, y_start+(j+1)*square_size, 
                                                             width=1, fill=config['fill'], outline=config['outline'], tags='grid')
    
    def fill_squares(self, cw):
        cw_locs = cw.getLocations()
        for loc in self.squares:
            if loc in cw_locs:
                square_coord = self.coords(self.squares[loc])
                text_coord = (square_coord[0] + square_coord[2])/2, (square_coord[1] + square_coord[3])/2
                # print(text_coord)
                self.create_text(text_coord[0], text_coord[1], text=cw_locs[loc], font=('Times', '24'), tags='fill')
            # else:
            #     self.itemconfigure(self.squares[loc], fill='black')

    def preview_squares(self, cw):
        cw_locs = cw.getLocations()
        cw_starts = {word.getLocation(0):i+1 for i,word in enumerate(cw.words)}
        x_start, y_start = self.x_pad*self.square_size, self.y_pad*self.square_size
        square_size = self.square_size
        for loc in self.squares:
            if loc in cw_locs:
                self.create_rectangle(x_start+loc[0]*square_size, y_start+loc[1]*square_size, 
                                                             x_start+(loc[0]+1)*square_size, y_start+(loc[1]+1)*square_size, 
                                                             width=2, fill='white smoke', outline='black', tags='fill')
                if loc in cw_starts:
                    x0, y0, x1, y1 = self.coords(self.squares[loc])
                    self.create_oval(x0+2, y0+2, (x0+x1)/2-2, (y0+y1)/2-2, tags='fill')
                    self.create_text(x1/4+3*x0/4, y1/4+3*y0/4, text=cw_starts[loc], tags='fill')

    def clear_fills(self):
        self.delete('fill')
        # for square_id in self.squares.values():
        #     self.itemconfigure(square_id, fill='') # Changing item attributes
    
    def clear_squares(self):
        self.delete('grid')
        self.squares = {}
    

if __name__ == '__main__':
    app = App()
    app.mainloop()
    
# %%
w = 'captain'
print(w.upper())



