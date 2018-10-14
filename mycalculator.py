import mywidget as mw
import solveequation as se


class MyCalculator:

    def __init__(self):

        self.equation = se.SolveEquation()
        self.myInterface = mw.MyInterface(self.equation)
        self.myInterface.mainWindow.mainloop()

