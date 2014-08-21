import tkinter as tk
import tkinter.filedialog as filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self,master)
        self.grid(sticky=tk.N+tk.W+tk.N+tk.E)
        self.createWidgets()
        self.pagelines = 20
        self.currentline=1
        self.endoffile = 0
        self.encoding = 'gbk'
        self.linelength = 20
        self.errorno = 0

    def createWidgets(self):
        self.text = tk.Text(self)
        self.text.grid(row=0,columnspan=2)

        self.open_button = tk.Button(self)
        self.open_button['text'] = 'open'
        self.open_button['command'] = self.open
        self.open_button.grid(row=1,column=0,sticky=tk.W)

        self.next_button = tk.Button(self)
        self.next_button['text'] = 'next'
        self.next_button['command'] = self.next
        self.next_button.grid(row=1,column=1,padx=1)

    def open(self):
        filename = filedialog.askopenfilename(parent=self)
        self.fp = open(filename,'rb')
        self.endoffile = 0
        self.text.delete('1.0','%d.end'%self.pagelines)
        for i in range(self.pagelines):
            line = self.readline() 
            if not line.isspace():
                self.text.insert('%d.0'%(i+1),line)
                self.currentline += 1
    
    def next(self):
        if self.endoffile == 0:
            self.text.delete('1.0','%d.end'%self.pagelines)
            for i in range(self.pagelines):
                line = self.readline() + '\n'
                if line:
                    self.text.insert('%d.0'%(i+1),line)
                    self.currentline += 1

    def readline(self):
        line = ''
        for j in range(self.linelength):
            char = self.DecodeChar()
            if char == '\n':
                break
            else:
                line += char
        return line

    def DecodeChar(self):
        data = self.fp.read(1)
        decode_flag = 0
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
        elif decode_flag == 2:
            return error_char

if __name__ == '__main__':

    root = tk.Tk()
    app = Application(master=root)
    app.master.title('ureader')
    app.mainloop()

