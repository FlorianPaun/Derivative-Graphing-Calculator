import Tkinter as tkinter


class Keyboard(tkinter.Frame):
    """Frame containing a calculator keyboard."""
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, bg='white')
        global pixel
        pixel = tkinter.PhotoImage(width=1, height=1)


        self.function = ""
        self.openBracketsCounter = 0
        self.closedBracketsCounter = 0

        # is split into 3 frames
        self.frameTop = tkinter.Frame(self, bg="white", width=283, height=70, highlightbackground="gray40", highlightthickness=2)
        self.frameTop.pack_propagate(False)
        self.frameTop.pack(side=tkinter.TOP, anchor=tkinter.N)

        self.frameMid = tkinter.Frame(self, bg="white")
        self.frameMid.pack(side=tkinter.TOP, anchor=tkinter.N)

        self.frameBottom = tkinter.Frame(self, bg="white", width=283, height=120)
        self.frameBottom.pack_propagate(False)
        self.frameBottom.pack(side=tkinter.BOTTOM, anchor=tkinter.S)

        self.create_widgets()

    def create_widgets(self):
        self.labelFx = tkinter.Label(self.frameTop, text=" f(x)= ", bg="white", font=("Segoe", 15, "normal"))
        self.labelFx.pack(side=tkinter.LEFT, anchor=tkinter.SW, pady=20)

        self.labelFunction = tkinter.Label(self.frameTop, text="", bg="white", font=("Segoe", 15, "normal"))
        self.labelFunction.pack(side=tkinter.LEFT, anchor=tkinter.SW, pady=20)

        # region Buttons
        self.buttonDelete = self.create_button(self.frameMid, "del", self.delete, (0,0))
        self.buttonDelete.config(bg="LightSalmon2")

        self.button7 = self.create_button(self.frameMid, "7", lambda: self.insert_number("7"), (1,0))
        self.button7.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button8 = self.create_button(self.frameMid, "8", lambda: self.insert_number("8"), (1,1))
        self.button8.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button9 = self.create_button(self.frameMid, "9", lambda: self.insert_number("9"), (1,2))
        self.button9.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button4 = self.create_button(self.frameMid, "4", lambda: self.insert_number("4"), (2,0))
        self.button4.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button5 = self.create_button(self.frameMid, "5", lambda: self.insert_number("5"), (2,1))
        self.button5.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button6 = self.create_button(self.frameMid, "6", lambda: self.insert_number("6"), (2,2))
        self.button6.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button1 = self.create_button(self.frameMid, "1", lambda: self.insert_number("1"), (3,0))
        self.button1.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button2 = self.create_button(self.frameMid, "2", lambda: self.insert_number("2"), (3,1))
        self.button2.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button3 = self.create_button(self.frameMid, "3", lambda: self.insert_number("3"), (3,2))
        self.button3.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.button0 = self.create_button(self.frameMid, "0", lambda: self.insert_number("0"), (4,1))
        self.button0.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.buttonPi = self.create_button(self.frameMid, "pi", lambda: self.insert_var("pi"), (4,0))
        self.buttonPi.config(font=("Segoe", 20, "bold"), bg="grey82")
        self.buttonDot = self.create_button(self.frameMid, ".", self.insert_dot, (4,2))
        self.buttonDot.config(font=("Segoe", 20, "bold"), bg="grey82")

        self.buttonBracketOpen = self.create_button(self.frameMid, "(", self.bracket_open, (1,3))
        self.buttonBracketOpen.config(width=25)

        self.buttonBracketClose = self.create_button(self.frameMid, ")", self.bracket_close, (1,4))
        self.buttonBracketClose.config(width=25)

        self.buttonMultiply = self.create_button(self.frameMid, "*", lambda: self.insert_operator("*"), (0,1))
        self.buttonDivide = self.create_button(self.frameMid, "/", lambda: self.insert_operator("/"), (0,2))
        self.buttonPlus = self.create_button(self.frameMid, "+", lambda: self.insert_operator("+"), (2,3))
        self.buttonPlus.grid(columnspan=2)
        self.buttonMinus = self.create_button(self.frameMid, "-", lambda: self.insert_operator("-"), (3,3))
        self.buttonMinus.grid(columnspan=2)
        self.buttonPower = self.create_button(self.frameMid, "^", lambda: self.insert_operator("^"), (0,3))
        self.buttonPower.grid(columnspan=2)
        self.buttonSqrt = self.create_button(self.frameMid, "sqrt()", lambda: self.insert_misc("sqrt("), (5,2))
        self.buttonSin = self.create_button(self.frameMid, "sin()", lambda: self.insert_misc("sin("), (5,0))
        self.buttonCos = self.create_button(self.frameMid, "cos()", lambda: self.insert_misc("cos("), (5,1))
        self.buttonX = self.create_button(self.frameMid, "x", lambda: self.insert_var("x"), (4,3))
        self.buttonX.grid(columnspan=2)
        self.buttonE = self.create_button(self.frameMid, "e", lambda: self.insert_var("e"), (5,3))
        self.buttonE.grid(columnspan=2)

        self.buttonStart = tkinter.Button(self.frameBottom, text="START", command=lambda: self.start())
        self.buttonStart.pack(side=tkinter.RIGHT, anchor=tkinter.NE, padx=20, pady=30)
        self.buttonStart.config(font=("Segoe", 20, "normal"), image=pixel, width=100, height=40, compound="c", relief=tkinter.FLAT, bg="pale green")

        self.buttonReset = tkinter.Button(self.frameBottom, text="RESET", command=lambda: self.reset())
        self.buttonReset.pack(side=tkinter.LEFT, anchor=tkinter.NW, padx=20, pady=30)
        self.buttonReset.config(font=("Segoe", 20, "normal"), image=pixel, width=100, height=40, compound="c", relief=tkinter.FLAT, bg="gray90")
        # endregion

    @staticmethod
    def create_button(frame, text, command, pos):
        button = tkinter.Button(frame, text=text, command=command)
        button.grid(row=pos[0], column=pos[1], padx=1, pady=1, columnspan=1)
        button.config(font=("Segoe", 20, "normal"), image=pixel, width=60, height=30, compound="c", relief=tkinter.FLAT, bg="gray90")
        return button

    def delete(self):
        """Deletes the last character or sin/cos/sqrt/pi from the string and updates the bracket counters if necesary"""
        if self.function != "":
            if self.function[-2:] == "pi":  # delete pi
                self.function = self.function[:-2]
            elif self.function[-4:] == "cos(" or self.function[-4:] == "sin(":  # delete sin( or cos(
                self.function = self.function[:-4]
                self.openBracketsCounter -= 1
            elif self.function[-5:] == "sqrt(":  # delete sqrt(
                self.function = self.function[:-5]
                self.openBracketsCounter -= 1
            elif self.function[-1] == "(":
                self.function = self.function[:-1]
                self.openBracketsCounter -= 1
            elif self.function[-1] == ")":
                self.function = self.function[:-1]
                self.closedBracketsCounter -= 1
            else:
                self.function = self.function[:-1]
            self.labelFunction.configure(text=self.function)

    @staticmethod
    def is_0(x):
        """Checks if the last number in the string is 0, returns boolean"""
        if x == "0":
            return True
        elif x[-1] == "0" and x[-2] in "/*-+^(":
                return True
        else:
            return False

    @staticmethod
    def is_decimal(x):
        """Checks if the last number in the string is already decimal, returns boolean"""
        is_decimal = False
        while not is_decimal and x != "":
            if x[-1] in "/*-+":
                return is_decimal
            elif x[-1] in ".":
                is_decimal = True
                return is_decimal
            x = x[:-1]
            if x == "":
                is_decimal = False
                return is_decimal

    def insert_dot(self):
        """Inserts ".", but only once in the same number"""
        if self.function == "":
            self.function = "0."
        elif self.function[-1] in ")xei":
            self.function = self.function + "*0."
        elif self.function[-1] in "*-/+(^":
            self.function = self.function + "0."
        elif self.function[-1] == ".":
            return
        elif self.is_decimal(self.function):
            return
        else:
            self.function = self.function + "."
        self.labelFunction.configure(text=self.function)

    def insert_number(self, n):
        """Inserts number n into the string"""
        if self.function == "":
            self.function = self.function + n
        elif self.function[-1] in ")xei":
            self.function = self.function + "*" + n
        elif self.is_0(self.function):
            self.function = self.function[:-1] + n
        else:
            self.function = self.function + n
        self.labelFunction.configure(text=self.function)

    def insert_operator(self, o):
        """For inserting + - * / or ^"""
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
        """For inserting sin(, cos( or sqrt("""
        if self.function == "" or self.function[-1] in "/*+-^(":
            self.function = self.function + misc
            self.openBracketsCounter += 1
        elif self.function[-1] in ".":
            self.function = self.function[:-1] + "*" + misc
            self.openBracketsCounter += 1
        elif self.function[-1] in "ex1234567890)i":
            self.function = self.function + "*" + misc
            self.openBracketsCounter += 1
        self.labelFunction.configure(text=self.function)

    def insert_var(self, v):
        """For inserting variables like pi, x and e"""
        if self.function == "":
            self.function = self.function + v
        elif self.function[-1] in "ex1234567890)i":
            self.function = self.function + "*" + v
        elif self.is_decimal(self.function):
            return
        elif self.function[-1] == ")":
            self.function = self.function + "*" + v
        elif self.is_0(self.function):
            self.function = self.function[:-1] + v
        else:
            self.function = self.function + v
        self.labelFunction.configure(text=self.function)

    def bracket_open(self):
        """Inserts ( into string and updates openBracketCounter"""
        if self.function == "":
            self.function = self.function + "("
            self.openBracketsCounter += 1
        elif self.function[-1] in "ex1234567890)i":
            self.function = self.function + "*("
            self.openBracketsCounter += 1
        else:
            self.function = self.function + "("
            self.openBracketsCounter += 1
        self.labelFunction.configure(text=self.function)

    def bracket_close(self):
        """Inserts ) into the string if there are already open brackets and updates openBracketCounter"""
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
        """Freezes all Button widgets in self.frameMid"""
        for widget in self.frameMid.winfo_children():
            if isinstance(widget, tkinter.Button):
                widget.config(state="disabled")
        self.buttonStart.config(state="disabled")

    def unfreeze_buttons(self):
        """Unfreezes all Button widgets in self.frameMid"""
        for widget in self.frameMid.winfo_children():
            if isinstance(widget, tkinter.Button):
                widget.config(state="normal")
        self.buttonStart.config(state="normal")

    def start(self):
        """Defined in main.py"""
        if self.function[-1] in "*^-+.":
            self.function = self.function[:-1]
            self.labelFunction.configure(text=self.function)

        if __name__ == "__main__":  # for debugging only
            self.freeze_buttons()
            print self.function
        else:
            try:
                start()  # defined in main.py
            except:
                pass

    def reset(self):
        """Defined in main.py"""
        if __name__ == "__main__":  # for debugging only
            self.unfreeze_buttons()
            self.function = ""
            self.openBracketsCounter = 0
            self.closedBracketsCounter = 0
            self.labelFunction.configure(text=self.function)
            print "Everything was reset."
        else:
            try:
                reset()  # defined in main.py
            except:
                pass


if __name__ == "__main__":
    root = tkinter.Tk()
    pixel = tkinter.PhotoImage(width=1, height=1)
    keyboard = Keyboard(root)
    keyboard.pack()
    root = tkinter.mainloop()
