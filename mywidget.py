import tkinter as tk
from tkinter import ttk


class MyInterface:
    def __init__(self, equation):

        # Window
        self.mainWindow = tk.Tk()
        self.mainWindow.title("MyCalculator")
        # Frame of Button & Entry
        self.staticFrame = tk.Frame(self.mainWindow)

        # Tips
        self.Label1 = tk.Label(self.staticFrame,
                               text="Tips:  And : &  Or : |  Not : ~  Xor : ^  ")

        # Output Data
        self.equation = equation
        self.truth_table = []
        self.variables = []
        self.all_answers = []
        self.all_value = []
        self.temp = 0
        self.cdnf = ''
        self.ccnf = ''

        # Input Data
        self.inputString = tk.StringVar()

        # Input Button
        self.inputButton = tk.Button(self.staticFrame,
                                     text='Done',
                                     fg='black',
                                     command=self.communicate,
                                     height=1,
                                     width=5,
                                     bd=3)

        # Input Box
        self.entryInputBox = tk.Entry(self.staticFrame,
                                      textvariable=self.inputString,
                                      relief='groove',
                                      borderwidth=3)
        self.clearButton = tk.Button(self.staticFrame,
                                     text='Clear',
                                     fg='black',
                                     command=self.clear_entry,
                                     height=1,
                                     width=5,
                                     bd=3)

        # Warning Windows and Text
        self.warning_window = None
        self.warning_text = ''

        # Output Box
        self.truthText = None

        self.paradigmMessage = None

        # Layout Control
        self.Label1.grid(row=0, column=0)
        self.staticFrame.grid(row=0, column=0)
        self.entryInputBox.grid(row=1)
        self.inputButton.grid(row=1, column=1, sticky=tk.E)
        self.clearButton.grid(row=1, column=2, sticky=tk.E)

        # Bind Enter Down Event
        self.entryInputBox.bind('<Return>', func=self.enter_communicate)

    def pass_data(self):

        # Input Check
        try:
            self.equation.process_equation(self.inputString.get())
        except NameError:
            self.output_warning("变量命名出错！")
            print("Name Wrong")
            print("Input again")
            return

        except TypeError:
            self.output_warning("类出错！")
            return

        except Exception:
            self.output_warning("出现未知字符！")
            return
        self.variables = [variable for variable in self.equation.variables]
        self.all_answers = self.equation.all_answers
        self.all_value = self.equation.all_value
        self.ccnf = self.equation.ccnf
        self.cdnf = self.equation.cdnf
        print(self.all_value)
        return

    # Exchange Data (widget with solveequation)
    def communicate(self):
        if self.entryInputBox.get() is not '':
            self.pass_data()
        if len(self.variables) != 1:
                self.output_table()
                self.output_paradigm()
        else:
            self.output_warning('   请不要调戏我！\n最少两个变量，谢谢！')
            self.equation.clear()
        return

    # Enter Down Function
    def enter_communicate(self, event):
        self.communicate()
        return

    # Truth table Output
    def output_table(self):

        # Delete the Last Visual Table
        if self.truthText is not None:
            self.truthText.destroy()
            self.truthText = None

        # Layout Change
        self.mainWindow.geometry((str((len(self.variables)+1) * 120)
                                 if (len(self.variables)+1) > 3 else '360')
                                 + 'x' +
                                 str(290 +
                                     int(40*(10*len(self.ccnf+self.cdnf)/(120*(len(self.variables)+1)))+80)))

        # Table
        self.truthText = ttk.Treeview(self.mainWindow,
                                      column=self.variables+[self.temp],
                                      show='headings',)
        self.truthText.column(self.temp, width=120, anchor='center')
        self.truthText.heading(self.temp, text='values')

        # Set up Variables
        for variable in self.variables:
            self.truthText.column(variable, width=120, anchor='center')
            self.truthText.heading(variable, text=str(variable))

        # Insert Data
        for times in range(len(self.all_value)):
            self.truthText.insert('', value=self.all_value[times], index=times)
        self.truthText.grid()
        self.mainWindow.minsize()
        self.equation.clear()
        return

    # Clear Entry
    def clear_entry(self):
        self.entryInputBox.delete('0', 'end')

    # Warning Windows Show
    def output_warning(self, txt):
        # Destroy the Former One
        if self.warning_window is not None:
            self.warning_window.destroy()
            self.warning_window = None

        # Warning Window
        self.warning_window = tk.Toplevel()
        self.warning_window.geometry('150x40')
        self.warning_text = tk.Text(master=self.warning_window)
        self.warning_text.insert(tk.INSERT, txt)
        self.warning_text.grid(sticky=tk.NSEW)
        self.warning_window.mainloop()

    def output_paradigm(self):
        # Destroy the Former One
        if self.paradigmMessage is not None:
            self.paradigmMessage.destroy()
            self.paradigmMessage = None

        # Paradigm Output
        self.paradigmMessage = tk.Message(self.mainWindow,
                                          text='析取范式:\n' +
                                               self.cdnf+'\n' +
                                               '合取范式:\n' +
                                               self.ccnf,
                                          font="微软雅黑",
                                          width=((len(self.variables)+0.5) * 120)
                                          )
        self.paradigmMessage.grid()

