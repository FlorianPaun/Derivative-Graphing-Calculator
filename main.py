import tkinter as tk
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr as parse_expr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Function:
    def __init__(self):
        self.function = ""

        self.x_values = np.arange(-20.0, 20.0, 0.1)
        for counter, value in enumerate(self.x_values):
            self.x_values[counter] = round(self.x_values[counter], 2)

        self.y_values = np.arange(-20.0, 20.0, 0.1)

        self.min_points = []
        self.max_points = []
        self.turning_points = []
        self.point_y_0 = []
        self.points_x_0 = []

    def reset(self):
        # x_values doesn't need to change
        self.function = ""
        self.y_values = np.arange(-20.0, 20.0, 0.1)
        self.min_points = []
        self.max_points = []
        self.turning_points = []
        self.point_y_0 = 0.0
        self.points_x_0 = []


class Derivative:
    def __init__(self):
        self.function = ""

        self.x_values = np.arange(-20.0, 20.0, 0.1)
        for counter, value in enumerate(self.x_values):
            self.x_values[counter] = round(self.x_values[counter], 2)

        self.y_values = np.arange(-20.0, 20.0, 0.1)

    def reset(self):
        # x_values doesn't need to change
        self.function = ""
        self.y_values = np.arange(-20.0, 20.0, 0.1)


class FunctionOperations:
    """Class of static methods, operations for working with functions"""

    @staticmethod
    def derive_function(f):
        """Returns the derivative of a function's expression, string>string"""
        d = str(sp.diff(f))
        return d

    @staticmethod
    def convert_to_sp(f):
        """Converts some characters in the expression with characters that sympy can work with"""
        f = f.replace("^", "**")
        f = f.replace("e", "E")
        return f

    @staticmethod
    def convert_from_sp(f):
        """Converts some characters from the sympy namespace to characters that the user is used to seeing"""
        f = f.replace("**", "^")
        f = f.replace("E", "e")
        f = f.replace(" ", "")
        f = f.replace("exp(x)", "e^x")
        return f

    @staticmethod
    def create_derivatives():
        """Creates the first 3 derivatives of f(x)"""
        dx_1.function = FunctionOperations.derive_function(fx.function)
        dx_2.function = FunctionOperations.derive_function(dx_1.function)
        dx_3.function = FunctionOperations.derive_function(dx_2.function)

    @staticmethod
    def calculate_y_values(x_values, y_values, function):
        """Calculates all y values by replacing x in the function's expression with every x value and parsing that
        using sympy.parse_expr()"""
        for counter, value in enumerate(x_values):
            f = function.replace("x", "(" + str(value) + ")")
            try:
                y_values[counter] = parse_expr(f)
            except:
                y_values[counter] = None
        return y_values

    @staticmethod
    def find_point_y_0(function):
        """Returns the point (0, y), as a list containing a tuple so that it is the same with the others"""
        function = function.replace("x", "(0)")
        point = []
        try:
            y_value = round(float(parse_expr(function)), 2)

            if y_value == int(y_value):  # in case of unnecessary float
                y_value = int(y_value)

            point.append((0, y_value))
            return point
        except:
            return

    @staticmethod
    def find_points_x_0(function):
        """Returns a list of x values by solving the equation f(x)=0 with sympy.solve"""
        function = sp.simplify(function)  # convert from string to an actual expression
        x = sp.Symbol("x")
        solutions = sp.solve(function, x)  # type list
        real_solutions = []

        for value in solutions: # I=i, eliminate all complex solutions
            if "I" not in str(value):
                real_solutions.append(value)

        for counter, value in enumerate(real_solutions): # in case we get a really long solution
            if len(str(value)) > 15:
                real_solutions[counter] = real_solutions[counter].evalf()
                real_solutions[counter] = round(real_solutions[counter], 2)

        return real_solutions

    @staticmethod
    def find_min_points(f, d1, d2):
        """Returns a list of tuples (x, y), the point(s) where f(x) has minimum values"""
        # find the x values where f'(x) = 0
        x_values = FunctionOperations.find_points_x_0(d1)
        x_min_values = []

        for x_value in x_values:  # replace each x value in f''(x), in this case dx2
            expr = d2.replace("x", "(" + str(x_value) + ")")
            if parse_expr(expr) > 0:  # f''(x) > 0 ==> min point, f''(x) < 0 ==> max point
                x_min_values.append(x_value)

        # now put the x values from the previous step into f(x)to find the y values and complete the min points
        min_points = []
        for x_value in x_min_values:
            expr = f.replace("x", "(" + str(x_value) + ")")
            y_value = parse_expr(expr)
            min_points.append((x_value, y_value))

        return min_points

    @staticmethod
    def find_max_points(f, d1, d2):
        """Returns a list of tuples (x, y), the point(s) where f(x) has maximum values"""
        # find the x values where f'(x) = 0
        x_values = FunctionOperations.find_points_x_0(d1)
        x_max_values = []

        for x_value in x_values:  # replace each x value in f''(x), in this case dx2
            expr = d2.replace("x", "(" + str(x_value) + ")")
            if parse_expr(expr) < 0:  # f''(x) > 0 ==> min point, f''(x) < 0 ==> max point
                x_max_values.append(x_value)

        # now put the x values from the previous step into f(x)to find the y values and complete the min points
        max_points = []
        for x_value in x_max_values:
            expr = f.replace("x", "(" + str(x_value) + ")")
            y_value = parse_expr(expr)
            max_points.append((x_value, y_value))

        return max_points

    @staticmethod
    def find_turning_points(f, d2, d3):
        """Returns the turning points of f as a list of tuples (x, y)"""
        turning_points = []
        # first find the solutions for f''(x)=0
        x_values = FunctionOperations.find_points_x_0(d2)

        for x_value in x_values:
            expr = d3.replace("x", "(" + str(x_value) + ")")
            if parse_expr(expr) != 0:  # if f'''(x) =/= 0 then it is a valid turning point
                # now put the x value into f(x)to find the y value and complete the turning point
                expr = f.replace("x", "(" + str(x_value) + ")")
                y_value = parse_expr(expr)
                turning_points.append((x_value, y_value))

        return turning_points


class Input(tk.Frame):
    function = ""
    openBracketsCounter = 0
    closedBracketsCounter = 0

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='white')

        self.frame_top = tk.Frame(self, bg="white", width=283, height=70, highlightbackground="gray40", highlightthickness=2)
        self.frame_top.pack_propagate(False)
        self.frame_top.pack(side=tk.TOP, anchor=tk.N)

        self.frame_mid = tk.Frame(self, bg="white")
        self.frame_mid.pack(side=tk.TOP, anchor=tk.N)

        self.frame_bottom = tk.Frame(self, bg="white", width=283, height=120)
        self.frame_bottom.pack_propagate(False)
        self.frame_bottom.pack(side=tk.BOTTOM, anchor=tk.S)

        self.label_fx = tk.Label(self.frame_top, text=" f(x)= ", bg="white", font=("Segoe", 15, "normal"))
        self.label_fx.pack(side=tk.LEFT, anchor=tk.SW, pady=20)

        self.labelFunction = tk.Label(self.frame_top, text="", bg="white", font=("Segoe", 15, "normal"))
        self.labelFunction.pack(side=tk.LEFT, anchor=tk.SW, pady=20)

        # region Buttons
        self.pixel = tk.PhotoImage(width=1, height=1)

        self.button_delete = tk.Button(self.frame_mid, text="del", command=lambda: self.delete())
        self.button_delete.grid(row=0, column=0, padx=1, pady=1)
        self.button_delete.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="LightSalmon2")

        self.button7 = tk.Button(self.frame_mid, text="7", command=lambda: self.insert_number(str(7)))
        self.button7.grid(row=1, column=0, padx=1, pady=1)
        self.button7.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button8 = tk.Button(self.frame_mid, text="8", command=lambda: self.insert_number(str(8)))
        self.button8.grid(row=1, column=1, padx=1, pady=1)
        self.button8.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button9 = tk.Button(self.frame_mid, text="9", command=lambda: self.insert_number(str(9)))
        self.button9.grid(row=1, column=2, padx=1, pady=1)
        self.button9.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button4 = tk.Button(self.frame_mid, text="4", command=lambda: self.insert_number(str(4)))
        self.button4.grid(row=2, column=0, padx=1, pady=1)
        self.button4.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button5 = tk.Button(self.frame_mid, text="5", command=lambda: self.insert_number(str(5)))
        self.button5.grid(row=2, column=1, padx=1, pady=1)
        self.button5.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button6 = tk.Button(self.frame_mid, text="6", command=lambda: self.insert_number(str(6)))
        self.button6.grid(row=2, column=2, padx=1, pady=1)
        self.button6.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button1 = tk.Button(self.frame_mid, text="1", command=lambda: self.insert_number(str(1)))
        self.button1.grid(row=3, column=0, padx=1, pady=1)
        self.button1.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button2 = tk.Button(self.frame_mid, text="2", command=lambda: self.insert_number(str(2)))
        self.button2.grid(row=3, column=1, padx=1, pady=1)
        self.button2.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button3 = tk.Button(self.frame_mid, text="3", command=lambda: self.insert_number(str(3)))
        self.button3.grid(row=3, column=2, padx=1, pady=1)
        self.button3.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button0 = tk.Button(self.frame_mid, text="0", command=lambda: self.insert_number(str(0)))
        self.button0.grid(row=4, column=0, columnspan=2, padx=1, pady=1)
        self.button0.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button_dot = tk.Button(self.frame_mid, text=".", command=lambda: self.insert_dot())
        self.button_dot.grid(row=4, column=2, padx=1, pady=1)
        self.button_dot.config(font=("Segoe", 20, "bold"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT, bg="gray82")

        self.button_bracket_open = tk.Button(self.frame_mid, text="(", command=lambda: self.bracket_open())
        self.button_bracket_open.grid(row=1, column=3, padx=1, pady=1)
        self.button_bracket_open.config(font=("Segoe", 20, "normal"), image=self.pixel, width=25, height=30, compound="c", relief=tk.FLAT)

        self.button_bracket_close = tk.Button(self.frame_mid, text=")", command=lambda: self.bracket_close())
        self.button_bracket_close.grid(row=1, column=4, padx=1, pady=1)
        self.button_bracket_close.config(font=("Segoe", 20, "normal"), image=self.pixel, width=25, height=30, compound="c", relief=tk.FLAT)

        self.button_multiply = tk.Button(self.frame_mid, text="*", command=lambda: self.insert_operator("*"))
        self.button_multiply.grid(row=0, column=1, padx=1, pady=1)
        self.button_multiply.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_divide = tk.Button(self.frame_mid, text="/", command=lambda: self.insert_operator("/"))
        self.button_divide.grid(row=0, column=2, padx=1, pady=1)
        self.button_divide.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_plus = tk.Button(self.frame_mid, text="+", command=lambda: self.insert_operator("+"))
        self.button_plus.grid(row=2, column=3, columnspan=2, padx=1, pady=1)
        self.button_plus.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_minus = tk.Button(self.frame_mid, text="-", command=lambda: self.insert_operator("-"))
        self.button_minus.grid(row=3, column=3, columnspan=2, padx=1, pady=1)
        self.button_minus.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_power = tk.Button(self.frame_mid, text="^", command=lambda: self.insert_operator("^"))
        self.button_power.grid(row=0, column=3, columnspan=2, padx=1, pady=1)
        self.button_power.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_sqrt = tk.Button(self.frame_mid, text="sqrt()", command=lambda: self.insert_misc("sqrt("))
        self.button_sqrt.grid(row=5, column=2, padx=1, pady=1)
        self.button_sqrt.config(font=("Segoe", 18, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_sin = tk.Button(self.frame_mid, text="sin()", command=lambda: self.insert_misc("sin("))
        self.button_sin.grid(row=5, column=0, padx=1, pady=1)
        self.button_sin.config(font=("Segoe", 18, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_cos = tk.Button(self.frame_mid, text="cos()", command=lambda: self.insert_misc("cos("))
        self.button_cos.grid(row=5, column=1, padx=1, pady=1)
        self.button_cos.config(font=("Segoe", 18, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_x = tk.Button(self.frame_mid, text="x", command=lambda: self.insert_var("x"))
        self.button_x.grid(row=4, column=3, columnspan=2, padx=1, pady=1)
        self.button_x.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_e = tk.Button(self.frame_mid, text="e", command=lambda: self.insert_var("e"))
        self.button_e.grid(row=5, column=3, columnspan=2, padx=1, pady=1)
        self.button_e.config(font=("Segoe", 20, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)

        self.button_start = tk.Button(self.frame_bottom, text="START", command=lambda: self.start())
        self.button_start.pack(side=tk.RIGHT, anchor=tk.NE, padx=20, pady=30)
        self.button_start.config(font=("Segoe", 20, "normal"), image=self.pixel, width=100, height=40, compound="c", relief=tk.FLAT, bg="pale green")

        self.button_reset = tk.Button(self.frame_bottom, text="RESET", command=lambda: self.reset_button())
        self.button_reset.pack(side=tk.LEFT, anchor=tk.NW, padx=20, pady=30)
        self.button_reset.config(font=("Segoe", 20, "normal"), image=self.pixel, width=100, height=40, compound="c", relief=tk.FLAT, bg="gray82")
        # endregion

    def delete(self):
        """Deletes the last character from the string that the user is typing"""
        if self.function != "":
            if self.function[-1] == "(":
                self.openBracketsCounter -= 1
            elif self.function[-1] == ")":
                self.closedBracketsCounter -= 1
            self.function = self.function[:-1]
            self.labelFunction.configure(text=self.function)

    @staticmethod
    def is_0(x):
        """Checks if the last number in the string is 0, returns boolean"""
        if x == "0":
            number_is_0 = True
            return number_is_0
        elif x[-1] == "0":
            if x[-1] == ".":
                number_is_0 = False
                return number_is_0
            x = x[:-1]
            if x[-1] in "/*-+":
                number_is_0 = True
                return number_is_0

    @staticmethod
    def is_decimal(x):
        """Checks if the last number in the string is already decimal, returns boolean"""
        decimal = False
        while not decimal and x != "":
            if x[-1] in "/*-+":
                return decimal
            elif x[-1] in ".":
                decimal = True
                return decimal
            x = x[:-1]
            if x == "":
                decimal = False
                return decimal

    def insert_dot(self):
        """Inserts ".", but only once in the same number"""
        if self.function == "":
            self.function = "0."
        elif self.function[-1] == ")":
            self.function = self.function + "*0."
        elif self.function[-1] in "*-/+(":
            self.function = self.function + "0."
        elif self.function[-1] == ".":
            return
        elif Input.is_decimal(self.function):
            return
        else:
            self.function = self.function + "."
        self.labelFunction.configure(text=self.function)

    def insert_number(self, n):
        if self.function == "":
            self.function = self.function + n
        elif self.function[-1] in ")x":
            self.function = self.function + "*" + n
        elif Input.is_0(self.function):
            self.function = self.function[:-1] + n
        else:
            self.function = self.function + n
        self.labelFunction.configure(text=self.function)

    def insert_operator(self, o):
        if self.function == "":
            if o == "-":
                self.function = self.function + o
            else:
                return
        elif self.function[-1] == "(":
            if o == "-":
                self.function = self.function + o
            else:
                return
        elif self.function[-1] in "*/-+.^":
            self.function = self.function[:-1] + o
        else:
            self.function = self.function + o
        self.labelFunction.configure(text=self.function)

    def insert_misc(self, misc):
        if self.function == "" or self.function[-1] in "/*+-^(":
            self.function = self.function + misc
            self.openBracketsCounter += 1
        elif self.function[-1] in ".":
            self.function = self.function[:-1] + "*" + misc
            self.openBracketsCounter += 1
        elif self.function[-1] in "ex1234567890)":
            self.function = self.function + "*" + misc
            self.openBracketsCounter += 1
        self.labelFunction.configure(text=self.function)

    def insert_var(self, v):
        if self.function == "":
            self.function = self.function + v
        elif self.function[-1] in "ex1234567890)":
            self.function = self.function + "*" + v
        elif Input.is_decimal(self.function):
            return
        elif self.function[-1] == ")":
            self.function = self.function + "*" + v
        elif Input.is_0(self.function):
            self.function = self.function[:-1] + v
        else:
            self.function = self.function + v
        self.labelFunction.configure(text=self.function)

    def bracket_open(self):
        if self.function == "":
            self.function = self.function + "("
            self.openBracketsCounter += 1
        elif self.function[-1] in "ex1234567890)":
            self.function = self.function + "*("
            self.openBracketsCounter += 1
        else:
            self.function = self.function + "("
            self.openBracketsCounter += 1
        self.labelFunction.configure(text=self.function)

    def bracket_close(self):
        if self.openBracketsCounter > self.closedBracketsCounter:
            if self.function[-1] in "/*-+.":
                self.function = self.function[:-1] + ")"
                self.closedBracketsCounter += 1
            elif self.function[-1] == "(":
                return
            else:
                self.function = self.function + ")"
                self.closedBracketsCounter += 1
            self.labelFunction.configure(text=self.function)

    def freeze_buttons(self):
        self.button0.config(state="disabled")
        self.button1.config(state="disabled")
        self.button2.config(state="disabled")
        self.button3.config(state="disabled")
        self.button4.config(state="disabled")
        self.button5.config(state="disabled")
        self.button6.config(state="disabled")
        self.button7.config(state="disabled")
        self.button8.config(state="disabled")
        self.button9.config(state="disabled")
        self.button_start.config(state="disabled")
        self.button_e.config(state="disabled")
        self.button_x.config(state="disabled")
        self.button_cos.config(state="disabled")
        self.button_sin.config(state="disabled")
        self.button_sqrt.config(state="disabled")
        self.button_power.config(state="disabled")
        self.button_minus.config(state="disabled")
        self.button_plus.config(state="disabled")
        self.button_multiply.config(state="disabled")
        self.button_divide.config(state="disabled")
        self.button_delete.config(state="disabled")
        self.button_dot.config(state="disabled")
        self.button_bracket_close.config(state="disabled")
        self.button_bracket_open.config(state="disabled")

    def unfreeze_buttons(self):
        self.button0.config(state="normal")
        self.button1.config(state="normal")
        self.button2.config(state="normal")
        self.button3.config(state="normal")
        self.button4.config(state="normal")
        self.button5.config(state="normal")
        self.button6.config(state="normal")
        self.button7.config(state="normal")
        self.button8.config(state="normal")
        self.button9.config(state="normal")
        self.button_start.config(state="normal")
        self.button_e.config(state="normal")
        self.button_x.config(state="normal")
        self.button_cos.config(state="normal")
        self.button_sin.config(state="normal")
        self.button_sqrt.config(state="normal")
        self.button_power.config(state="normal")
        self.button_minus.config(state="normal")
        self.button_plus.config(state="normal")
        self.button_multiply.config(state="normal")
        self.button_divide.config(state="normal")
        self.button_delete.config(state="normal")
        self.button_dot.config(state="normal")
        self.button_bracket_close.config(state="normal")
        self.button_bracket_open.config(state="normal")

    def reset_button(self):
        self.unfreeze_buttons()
        frame_graph.reset_graph()
        self.function = ""
        self.openBracketsCounter = 0
        self.closedBracketsCounter = 0
        self.labelFunction.configure(text=self.function)
        frame_output.clear()
        fx.reset()
        dx_1.reset()
        dx_2.reset()
        dx_3.reset()

    def start(self):
        try:
            if self.openBracketsCounter == self.closedBracketsCounter and self.function != "":
                fx.function = FunctionOperations.convert_to_sp(self.function)
                FunctionOperations.create_derivatives()
                fx.y_values = FunctionOperations.calculate_y_values(fx.x_values, fx.y_values, fx.function)
                dx_1.y_values = FunctionOperations.calculate_y_values(dx_1.x_values, dx_1.y_values, dx_1.function)
                dx_2.y_values = FunctionOperations.calculate_y_values(dx_2.x_values, dx_2.y_values, dx_2.function)
                dx_3.y_values = FunctionOperations.calculate_y_values(dx_3.x_values, dx_3.y_values, dx_3.function)
                frame_graph.redraw_all()
                frame_graph.create_function_buttons()
                fx.point_y_0 = FunctionOperations.find_point_y_0(fx.function)
                for value in FunctionOperations.find_points_x_0(fx.function):
                    fx.points_x_0.append((value, 0))
                fx.min_points = FunctionOperations.find_min_points(fx.function, dx_1.function, dx_2.function)
                fx.max_points = FunctionOperations.find_max_points(fx.function, dx_1.function, dx_2.function)
                fx.turning_points = FunctionOperations.find_turning_points(fx.function, dx_2.function, dx_3.function)
                Output.update_output(frame_output)

                self.freeze_buttons()
        except:
            pass


class Output(tk.Frame):
    """Frame with a message widget containing the results"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=500, height=600, bg="white")
        self.pack_propagate(False)
        self.text = ""
        self.message = tk.Message(self, font=("Segoe", 14, "normal"), text="", bg="white", width=450)
        self.message.pack()

    def update_output(self):
        self.text += "\n"

        if fx.function != "0":
            self.text += "f(x) = " + FunctionOperations.convert_from_sp(fx.function) + "\n\n"
        if dx_1.function != "0":
            self.text += "f'(x) = " + FunctionOperations.convert_from_sp(dx_1.function) + "\n\n"
        if dx_2.function != "0":
            self.text += "f''(x) = " + FunctionOperations.convert_from_sp(dx_2.function) + "\n\n"
        if dx_3.function != "0":
            self.text += "f'''(x) = " + FunctionOperations.convert_from_sp(dx_3.function) + "\n\n\n"

        if len(fx.point_y_0) == 1:
            self.text += "f(x) schneidet die y-Achse an der Stelle:  "
            for point in fx.point_y_0:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        else:
            self.text += "f(x) schneidet die y-Achse nicht.\n\n"

        if len(fx.points_x_0) == 1:
            self.text += "f(x) schneidet die x-Achse an der Stelle:  "
            for point in fx.points_x_0:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(fx.points_x_0) == 0:
            self.text += "f(x) schneidet die x-Achse nicht.\n\n"
        elif len(fx.points_x_0) > 1:
            self.text += "f(x) schneidet die x-Achse an den Stellen:\n  "
            for point in fx.points_x_0:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")  "
            self.text += "\n\n"

        if len(fx.min_points) == 1:
            self.text += "f(x) hat den Tiefpunkt:  "
            for point in fx.min_points:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(fx.min_points) == 0:
            self.text += "f(x) hat keine Tiefpunkte.\n\n"
        elif len(fx.min_points) > 1:
            self.text += "f(x) hat folgende Tiefpunkte:\n  "
            for point in fx.min_points:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")  "
            self.text += "\n\n"

        if len(fx.max_points) == 1:
            self.text += "f(x) hat den Hochpunkt:  "
            for point in fx.max_points:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(fx.max_points) == 0:
            self.text += "f(x) hat keine Hochpunkte.\n\n"
        elif len(fx.max_points) > 1:
            self.text += "f(x) hat folgende Hochpunkte:\n  "
            for point in fx.max_points:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")  "
            self.text += "\n\n"

        if len(fx.turning_points) == 1:
            self.text += "f(x) hat den Wendepunkt:  "
            for point in fx.turning_points:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(fx.turning_points) == 0:
            self.text += "f(x) hat keine Wendepunkte.\n\n"
        elif len(fx.turning_points) > 1:
            self.text += "f(x) hat folgende Wendepunkte:\n  "
            for point in fx.turning_points:
                self.text += "(" + str(point[0]) + " | " + str(point[1]) + ")  "
            self.text += "\n\n"

        if "cos" in self.text or "sin" in self.text or "pi" in self.text:  # in case of sin and cos
            self.text += "\nIn dem Fall von trigonometrischen Funktionen werden nicht alle Punkte angezeigt!"
        self.message.configure(text=self.text)

    def clear(self):
        self.text = ""
        self.message.configure(text="")


class Graph(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="white")
        self.zoom_values = [-4.0, 4.0, -4.0, 4.0]  # x-left, x-right, y-down, y-up
        self.line_styles = ["-", "-", "-", "-"]
        self.graph = Figure(figsize=(6, 6), dpi=100)
        self.graph.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98)

        self.axes = self.graph.add_subplot(111)
        self.create_axis()

        self.canvas = FigureCanvasTkAgg(self.graph, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP)

        # region Buttons
        self.pixel = tk.PhotoImage(width=1, height=1)

        self.button_zoom_in = tk.Button(self, text="+", command=lambda: self.zoom_in())
        self.button_zoom_in.config(font=("Segoe", 25, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)
        self.button_zoom_in.pack(side=tk.RIGHT)

        self.button_zoom_out = tk.Button(self, text="-", command=lambda: self.zoom_out())
        self.button_zoom_out.config(font=("Segoe", 35, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)
        self.button_zoom_out.pack(side=tk.RIGHT, padx=5)
        # endregion

    def create_function_buttons(self):
        self.button_fx = tk.Button(self, text="f(x)", command=lambda: self.switch_line_style(0))
        self.button_fx.config(font=("Segoe", 15, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)
        if fx.function != "0":
            self.button_fx.pack(side=tk.LEFT, padx=5)

        self.button_dx_1 = tk.Button(self, text="f '(x)", command=lambda: self.switch_line_style(1))
        self.button_dx_1.config(font=("Segoe", 15, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)
        if dx_1.function != "0":
            self.button_dx_1.pack(side=tk.LEFT, padx=5)

        self.button_dx_2 = tk.Button(self, text="f ''(x)", command=lambda: self.switch_line_style(2))
        self.button_dx_2.config(font=("Segoe", 15, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)
        if dx_2.function != "0":
            self.button_dx_2.pack(side=tk.LEFT, padx=5)

        self.button_dx_3 = tk.Button(self, text="f '''(x)", command=lambda: self.switch_line_style(3))
        self.button_dx_3.config(font=("Segoe", 15, "normal"), image=self.pixel, width=60, height=30, compound="c", relief=tk.FLAT)
        if dx_3.function != "0":
            self.button_dx_3.pack(side=tk.LEFT, padx=5)

    def create_axis(self):
        self.axes.set(xlim=(self.zoom_values[0], self.zoom_values[1]), ylim=(self.zoom_values[2], self.zoom_values[3]))
        self.axes.grid(True)
        self.axes.spines["left"].set_position("zero")
        self.axes.spines["bottom"].set_position("zero")
        self.axes.spines["right"].set_color("none")
        self.axes.spines["top"].set_color("none")
        self.axes.xaxis.set_ticks_position("both")
        self.axes.yaxis.set_ticks_position("both")

    def zoom_out(self):
        counter = 0
        if -20.0 < self.zoom_values[0] <= -1.0:
            for value in self.zoom_values:
                if value < 0:
                    self.zoom_values[counter] -= 1.0
                elif value > 0:
                    self.zoom_values[counter] += 1.0
                counter += 1
        self.redraw_all()

    def zoom_in(self):
        counter = 0
        if -20.0 <= self.zoom_values[0] < -1.0:
            for value in self.zoom_values:
                if value < 0:
                    self.zoom_values[counter] += 1.0
                elif value > 0:
                    self.zoom_values[counter] -= 1.0
                counter += 1
        self.redraw_all()

    def switch_line_style(self, n):
        if self.line_styles[n] == "-":
            self.line_styles[n] = "None"
        elif self.line_styles[n] == "None":
            self.line_styles[n] = "-"
        self.redraw_all()

    def redraw_all(self):
        self.axes.clear()
        self.create_axis()
        if fx.function != "0" and fx.function != "":
            if self.line_styles[0] == "-":
                self.axes.plot(fx.x_values, fx.y_values, self.line_styles[0], label="f(x)", color="b")
            else:
                self.axes.plot(fx.x_values, fx.y_values, self.line_styles[0], label="f(x)")
            if dx_1.function != "0":
                if self.line_styles[1] == "-":
                    self.axes.plot(dx_1.x_values, dx_1.y_values, self.line_styles[1], label="f'(x)", color="r")
                else:
                    self.axes.plot(dx_1.x_values, dx_1.y_values, self.line_styles[1], label="f'(x)")
                if dx_2.function != "0":
                    if self.line_styles[2] == "-":
                        self.axes.plot(dx_2.x_values, dx_2.y_values, self.line_styles[2], label="f''(x)", color="y")
                    else:
                        self.axes.plot(dx_2.x_values, dx_2.y_values, self.line_styles[2], label="f''(x)")
                    if dx_3.function != "0":
                        if self.line_styles[3] == "-":
                            self.axes.plot(dx_3.x_values, dx_3.y_values, self.line_styles[3], label="f'''(x)", color="m")
                        else:
                            self.axes.plot(dx_3.x_values, dx_3.y_values, self.line_styles[3], label="f'''(x)")
        self.axes.legend(loc='lower left')
        self.canvas.draw()

    def reset_graph(self):
        self.zoom_values = [-4.0, 4.0, -4.0, 4.0]  # x-left, x-right, y-down, y-up
        self.line_styles = ["-", "-", "-", "-"]
        self.axes.clear()
        self.create_axis()
        self.canvas.draw()
        self.button_fx.destroy()
        self.button_dx_1.destroy()
        self.button_dx_2.destroy()
        self.button_dx_3.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graphing calculator")
    root.config(bg="white")
    fx = Function()
    dx_1 = Derivative()
    dx_2 = Derivative()
    dx_3 = Derivative()
    frame_input = Input(root)
    frame_output = Output(root)
    frame_graph = Graph(root)
    frame_input.pack(side=tk.LEFT, anchor=tk.NW)
    frame_output.pack(side=tk.LEFT, anchor=tk.NW)
    frame_graph.pack(side=tk.LEFT, anchor=tk.NW)
    root.mainloop()


# TO DO:
# Bug with e^x
