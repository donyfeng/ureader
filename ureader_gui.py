from tkinter import *
from tkinter.filedialog import askopenfilename

class Ureader:
    def __init__(self, master):
        frame = Frame(master)
        
        self.label = Label(frame, text='   ')

        self.text = Text(frame,  relief=GROOVE, background='white', padx=10, pady=10)
        self.text.bind('<1>', self.set_focus)
        self.text.configure(state=DISABLED)
        self.text.pack(side=TOP,expand=YES, fill=BOTH)

        pre = Button(frame, text='PRE', height=2, width=8)
        pre.configure(command=self.pre)
        pre.pack(side=LEFT, expand=NO, fill=BOTH)

        askopen = Button(frame, text='OPEN',height=2, width=8)
        askopen.configure(command=self.openfile)
        askopen.pack(side=LEFT, expand=NO, fill=BOTH)

        nextpage = Button(frame, text='NEXT',height=2, width=8)
        nextpage.configure(command=self.nextpage)
        nextpage.pack(side=LEFT, expand=NO, fill=BOTH)

        option = Button(frame, text='OPTION',height=2, width=8)
        option.configure(command=self.option)
        option.pack(side=LEFT, expand=NO, fill=BOTH)

        frame.pack(side=LEFT, expand=YES,fill=BOTH)

        self.init_reader()

    def set_focus(self, event):
        self.text.focus_set()

    def option(self):
        op = Toplevel(root)
        op1 = StringVar()
        op2 = IntVar()
        op3 = IntVar()
        op4 = StringVar()
        op5 = StringVar()
        op1.set(self.encoding)
        op2.set(self.linenum)
        op3.set(self.columnnum)
        op4.set(self.text['background'])
        op5.set(self.text['foreground'])

        L1 = Label(op, text='input encoding:')
        L1.grid(row=0, column=0,sticky=W)
        E1 = Entry(op, textvariable=op1)
        E1.grid(row=0, column=1)

        L2 = Label(op, text='input line num:')
        L2.grid(row=1, column=0,sticky=W)
        E2 = Entry(op, textvariable=op2)
        E2.grid(row=1, column=1)

        L3 = Label(op, text='input column num:')
        L3.grid(row=2, column=0,sticky=W)
        E3 = Entry(op, textvariable=op3)
        E3.grid(row=2, column=1)

        L4 = Label(op, text='input back ground:')
        L4.grid(row=3, column=0,sticky=W)
        E4 = Entry(op, textvariable=op4)
        E4.grid(row=3, column=1)

        L5 = Label(op, text='input fore ground:')
        L5.grid(row=4, column=0,sticky=W)
        E5 = Entry(op, textvariable=op5)
        E5.grid(row=4, column=1)

        B1 = Button(op, text='Submit', command = 
                lambda s=self: (s.init_reader(op1.get(),op2.get(),op3.get()), s.text.configure(background=op4.get()), s.text.configure(foreground=op5.get())))
        B1.grid(row=5,column=0)


    def openfile(self):
        self.filename = askopenfilename()
        self.label.configure(text=self.filename)
        try:
            self.fp = open(self.filename, 'rb')
        except:
            pass
        else:
            self.nextpage()

    def init_reader(self,encoding='gbk', linenum=10, columnnum=40):
        self.encoding   = encoding
        self.linenum    = linenum
        self.columnnum  = columnnum
        self.linebreaker    = '\n'
        self.error_char     = '??'

    def decode_char(self):
        decode_flag = 0
        data =self.fp.read(1)

        while decode_flag == 0:
            try:
                char = data.decode(self.encoding)
            except UnicodeError as E:
                if E.reason == "incomplete multibyte sequence":
                    data += self.fp.read(1)
                else:
                    decode_flag = 2
            else:
                decode_flag = 1

        if decode_flag == 1:
            return char
        else:
            return self.error_char

    def readlines(self):
        for i in range(self.linenum):
            line = ''
            while not line or line.isspace():
                for j in range(self.columnnum):
                    char = self.decode_char()
                    if char == '\n':
                        break
                    else:
                        line += char
            self.text.insert(END,line + self.linebreaker)
            self.text.insert(END,'\n')

    def pre(self):
        if self.fp:
            self.fp.seek(self.pre_pos)

            self.text.configure(state=NORMAL)
            self.text.delete('1.0',END)
            self.readlines()
            self.text.configure(state=DISABLED)

    def nextpage(self):
        if self.fp:
            self.pre_pos = self.fp.tell()

            self.text.configure(state=NORMAL)
            self.text.delete('1.0',END)
            self.readlines()
            self.text.configure(state=DISABLED)

root = Tk()
ureader = Ureader(root)
root.mainloop()
