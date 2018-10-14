import pyeda.inter as p
import re
import tkinter

class SolveEquation:

    def __init__(self):
        # Equation_Expression
        self.propositional_str = ''
        self.propositional_formula = None

        # All TRUTH Value (uncompleted)
        self.truth_dic = {}

        # Variables
        self.variables = []
        self.number_variables = int

        # Store the Uncompleted Variables
        self.uncompleted_variables = []

        # Variables & Function Values
        self.all_value = []

        # All answers
        self.all_answers = []

        # ∨∧ formula
        self.ccnf = ''
        self.cdnf = ''

        # Warning Window
        self.warning_window = None
        self.warning_text = ''

    def process_equation(self, eq):
        '''(a&b)|(a&c)|(b&c)'''
        self.propositional_str = eq

        if not eq:
            return
        self.check_input()

        self.truth_dic = list(self.propositional_formula.satisfy_all())

        self.get_variable()

        # Number of Variables
        self.number_variables = len(self.variables)
        self.variables.sort(reverse=True)

        self.get_all_value()
        self.to_ccnf()
        self.to_cdnf()

    # Put variables in List
    def get_variable(self):
        for i in self.truth_dic:
            for key, value in i.items():
                if key not in self.variables:
                    self.variables.append(key)

    # Input Check
    def check_input(self):

        try:
            self.propositional_formula = p.expr(self.propositional_str)

        except NameError:
            raise NameError

        except TypeError:
            raise TypeError

        except Exception:
            raise Exception

    # Clear All properties of the Equation
    def clear(self):
        self.propositional_str = ''
        self.propositional_formula = None

        # All Truth Value (uncompleted)
        self.truth_dic = {}

        # Variables
        self.variables = []
        self.number_variables = int

        self.ccnf = ''
        self.cdnf = ''

    # Get Truth Table(In the form of List)
    def get_all_value(self):
        self.all_value = str(p.expr2truthtable(self.propositional_formula)).split('\n')
        self.all_value = self.all_value[1:-1]

        for counter in range(len(self.all_value)):
            self.all_value[counter] = re.findall(r'[\w]+', self.all_value[counter])

        self.all_answers = [x for lst in self.all_value
                            for x in lst[-1]]

    def item_get(self, index, factor):

        # Record Variable index
        variable_num = 0
        temp = '('

        '''(a&b)|(a&c)|(b&c)'''
        #  合取范式每个最大项
        if factor == 0:
            for value in self.all_value[index][0:-1]:
                if value == '0':
                    temp = temp + '(~' + str(self.variables[variable_num])+')'
                else:
                    temp = temp + str(self.variables[variable_num])
                if variable_num != len(self.variables) - 1:
                    temp = temp + '∨'
                variable_num = variable_num + 1

        # 析取范式每个最小项
        elif factor == 1:
            for value in self.all_value[index][0:-1]:
                if value == '0':
                    temp = temp + '(~' + str(self.variables[variable_num])+')'
                else:
                    temp = temp + str(self.variables[variable_num])
                if variable_num != len(self.variables) - 1:
                    temp = temp + '∧'
                variable_num = variable_num + 1
        temp = temp + ')'
        return temp

    # ∧
    def to_ccnf(self):
        indexes = []
        index = 0
        while index < len(self.all_answers):
            if self.all_answers[index] == '0':
                indexes.append(index)
            index = index+1
        for index in indexes:
            self.ccnf = self.ccnf + self.item_get(index, 0)
            if index != indexes[-1]:
                self.ccnf = self.ccnf + '∧'

    # ∨
    def to_cdnf(self):
        indexes = []
        index = 0
        while index < len(self.all_answers):
            if self.all_answers[index] == '1':
                indexes.append(index)
            index = index+1
        for index in indexes:
            self.cdnf = self.cdnf + self.item_get(index, 1)
            if index != indexes[-1]:
                self.cdnf = self.cdnf + '∨'

    def output_warning(self, txt):
        self.warning_window = tkinter.Toplevel()
        self.warning_window.geometry('150x40')
        self.warning_text = tkinter.Text(master=self.warning_window)
        self.warning_text.insert(tkinter.INSERT, txt)
        self.warning_text.grid(sticky=tkinter.NSEW)
        self.warning_window.mainloop()
