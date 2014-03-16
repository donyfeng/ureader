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
        self.encoding = 'utf-8'
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
            if line:
                self.text.insert('%d.0'%(i+1),str(self.currentline)+'\t'+line)
                self.currentline += 1
            else:
                self.endoffile = 1
    
    def next(self):
        if self.endoffile == 0:
            self.text.delete('1.0','%d.end'%self.pagelines)
            for i in range(self.pagelines):
                line = self.readline()
                if line:
                    self.text.insert('%d.0'%(i+1),str(self.currentline)+'\t'+line)
                    self.currentline += 1
                else:
                    self.endoffile = 1

    def readline(self):
        line = ''
        while 1:
            c = self.fp.read(1)
            a = ''
            try:
                a = c.decode(self.encoding)
            except:
                c += self.fp.read(1)
                try:
                    a = c.decode(self.encoding)
                except:
                    self.errorno += 1
                    a = '??'
                line += a
            else:
                line += a
            if len(line) >= self.linelength or a == '\n':
                if a == '\n':
                    return line
                else:
                    return line+'\n'


if __name__ == '__main__':

    root = tk.Tk()
    app = Application(master=root)
    app.master.title('ureader')
    app.mainloop()

