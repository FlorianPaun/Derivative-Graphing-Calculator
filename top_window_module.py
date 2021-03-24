# coding=utf-8
import Tkinter as tkinter

from sympy.parsing.sympy_parser import parse_expr


class TangentAndNormalWindow:
    """Opens a Tkinter Toplevel Widget. Reads the coordinates of a point, then calculates the tangent and normal in that
     point, if the point is part of the graph of the given function."""
    def __init__(self, window, function, derivative):
        top = tkinter.Toplevel(window)
        top.resizable(False, False)
        top.geometry("224x300")
        top.title(" ")
        top.attributes('-topmost', 'true')  # always on top

        self.function = function
        self.derivative = derivative

        self.create_widgets(top)

    def create_widgets(self, place):
        self.pixel = tkinter.PhotoImage(width=1, height=1)  # for button scaling

        self.label_instructions = tkinter.Label(place, font=("Segoe", 10, "normal"), text="Geben Sie den Punkt ein:")
        self.label_instructions.pack()

        self.label_brackets = tkinter.Label(place, font=("Segoe", 20, "normal"), text="(            |            )")
        self.label_brackets.pack()

        self.entry_x = tkinter.Entry(place, font=("Segoe", 20, "normal"), width="5", justify=tkinter.CENTER)
        self.entry_x.place(x=25, y=25)
        self.entry_y = tkinter.Entry(place, font=("Segoe", 20, "normal"), width="5", justify=tkinter.CENTER)
        self.entry_y.place(x=119, y=25)

        self.start_button = tkinter.Button(place, font=("Segoe", 12, "normal"), text="START", bg="pale green",
                                           relief=tkinter.FLAT, command=lambda: self.start())
        self.start_button.pack(pady=10)

        self.label_tangent = tkinter.Label(place, font=("Segoe", 12, "normal"), text="")
        self.label_tangent.pack()
        self.label_normal = tkinter.Label(place, font=("Segoe", 12, "normal"), text="")
        self.label_normal.pack()

        self.reset_button = tkinter.Button(place, font=("Segoe", 12, "normal"), text="RESET", bg="LightSalmon2",
                                           relief=tkinter.FLAT, command=lambda: self.reset())
        self.reset_button.pack(side=tkinter.BOTTOM, pady=10)
        self.reset_button.config(state="disabled")

    def read_values(self):
        """Reads x and y from the entry widgets, if possible"""
        try:
            x = self.entry_x.get()  # read x and y from entry widgets and convert them to floats
            y = self.entry_y.get()
            x = float(x)
            y = float(y)
            return x, y
        except:
            return None, None

    @staticmethod
    def point_is_on_graph(function, x, y):
        """Checks if x | y is on the graph of the function by comparing f(x) with y, returns boolean"""
        expr = function.replace("x", str(x))
        expr = expr.replace("^", "**")  # sympy cannot work with "^"
        expr = expr.replace("e", "E")
        if y == parse_expr(expr):
            return True
        else:
            return False

    def start(self):
        """Function of the start button"""
        x, y = self.read_values()
        if x is not None and y is not None:
            if self.point_is_on_graph(self.function, x, y):
                tangent, normal = self.calculate_tangent_and_normal(self.derivative, x, y)
                self.label_tangent.config(text="Tangente:\n" + tangent + "\n")
                self.label_normal.config(text="Normale:\n" + normal + "\n")
            else:
                self.label_tangent.config(text="Der Punkt liegt nicht\nauf dem Graph von f(x).")
        else:
            self.label_tangent.config(text="Ungültige Eingabe.")
        self.start_button.config(state="disabled", bg="LightSalmon2")
        self.reset_button.config(state="normal", bg="pale green")

    def reset(self):
        """Function of the reset button, resets certain widgets"""
        self.entry_x.delete(0, 'end')
        self.entry_y.delete(0, 'end')
        self.label_tangent.config(text="")
        self.label_normal.config(text="")
        self.start_button.config(state="normal", bg="pale green")
        self.reset_button.config(state="disabled", bg="LightSalmon2")


    @staticmethod
    def build_tangent(m, b):
        """Returns a string containing the tangent m*x+b"""
        if m == 0:  # building the tangent
            if b == 0:
                tangent = "0"
            else:
                tangent = str(b)
        elif m == 1:
            tangent = "x"
            if b < 0:
                tangent += str(b)
            elif b > 0:
                tangent += "+" + str(b)
        else:
            tangent = str(m) + "*x"
            if b < 0:
                tangent += str(b)
            elif b > 0:
                tangent += "+" + str(b)
        return tangent

    def calculate_tangent_and_normal(self, derivative, x, y):
        """Returns the tangent and the normal as strings"""
        # tangent
        expr = derivative.replace("x", str(x))
        expr = expr.replace("^", "**")  # sympy cannot work with "^"
        expr = expr.replace("e", "E")
        m = round(parse_expr(expr), 2)  # calculate slope by calculating f'(x)
        if m == int(m):  # remove unnecessary float
            m = int(m)
        b = round(y - m * x, 2)  # b=y-m*x
        if b == int(b):  # remove unnecessary float
            b = int(b)
        tangent = self.build_tangent(m, b)

        # normal
        if m == 0:
            normal = "In diesem Punkt kann keine\nNormale berechnet werden."
        else:
            m = round(-1.0 / m, 2)
            if m == int(m):  # remove unnecessary float
                m = int(m)
            b = round(y - m * x, 2)  # b=y-m*x
            if b == int(b):  # remove unnecessary float
                b = int(b)
            normal = self.build_tangent(m, b)

        return tangent, normal

    @staticmethod
    def destroy_all_toplevels(window):
        """Destroys all widgets of window that are Toplevel"""
        for widget in window.winfo_children():
            if isinstance(widget, tkinter.Toplevel):
                widget.destroy()


if __name__ == "__main__":
    def open_toplevel():
        TangentAndNormalWindow.destroy_all_toplevels(root)  # destroy all existing toplevels
        toplevel = TangentAndNormalWindow(root, "x^6 - x^4", "6*x^5 - 4*x^3")
        return toplevel

    root = tkinter.Tk()

    button = tkinter.Button(root, text="Open Top Level Window", command=lambda: open_toplevel())
    button.pack()

    root = tkinter.mainloop()
