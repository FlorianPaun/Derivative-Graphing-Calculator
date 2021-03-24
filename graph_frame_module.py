# coding=utf-8
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tkinter

class Graph(tkinter.Frame):
    def __init__(self, parent, f, d1, d2, d3):
        self.f = f
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        tkinter.Frame.__init__(self, parent, bg="white")
        self.xlim = (-4.1, 4.1)  # default x-left, x-right
        self.ylim = (-4.1, 4.1)  # default y-down, y-up
        self.line_styles = ["-", "-", "None", "None"]
        self.graph = Figure(figsize=(6, 6), dpi=100)
        self.graph.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98)

        self.axis = self.graph.add_subplot(111)
        self.create_axis()

        self.info_label = tkinter.Label(self, font=("Segoe", 10, "normal"), bg="white", justify=tkinter.LEFT,
                                   text="Mit der linke Maustaste verschieben Sie den Graph.\n"
                                        "Mit STRG + rechte Maustaste ändern Sie die Größe des Graphs.")
        self.info_label.pack(side=tkinter.TOP, anchor=tkinter.CENTER)

        self.canvas = FigureCanvasTkAgg(self.graph, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP)

        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.place(x=1400, y=0)
        toolbar.pan()

        self.pixel = tkinter.PhotoImage(width=1, height=1)  # for buttons

    def create_function_buttons(self):
        """Creates the buttons used to hide a functions from the graph."""
        if self.d3.function != "0":
            self.button_dx_3 = tkinter.Button(self, text="f '''(x)", command=lambda: self.switch_line_style(3))
            self.button_dx_3.config(font=("Segoe", 15, "normal"), image=self.pixel,
                                    width=60, height=30, compound="c", relief=tkinter.FLAT)
            self.button_dx_3.pack(side=tkinter.RIGHT, padx=5)
        if self.d2.function != "0":
            self.button_dx_2 = tkinter.Button(self, text="f ''(x)", command=lambda: self.switch_line_style(2))
            self.button_dx_2.config(font=("Segoe", 15, "normal"), image=self.pixel,
                                    width=60, height=30, compound="c", relief=tkinter.FLAT)
            self.button_dx_2.pack(side=tkinter.RIGHT, padx=5)
        if self.d1.function != "0":
            self.button_dx_1 = tkinter.Button(self, text="f '(x)", command=lambda: self.switch_line_style(1))
            self.button_dx_1.config(font=("Segoe", 15, "normal"), image=self.pixel,
                                    width=60, height=30, compound="c", relief=tkinter.FLAT)
            self.button_dx_1.pack(side=tkinter.RIGHT, padx=5)
        if self.f.function != "0":
            self.button_fx = tkinter.Button(self, text="f(x)", command=lambda: self.switch_line_style(0))
            self.button_fx.config(font=("Segoe", 15, "normal"), image=self.pixel,
                                  width=60, height=30, compound="c", relief=tkinter.FLAT)
            self.button_fx.pack(side=tkinter.RIGHT, padx=5)

            self.buttons_label = tkinter.Label(self, font=("Segoe", 12, "normal"),
                                          text="Funktionen ein- und ausblenden:", bg="white")
            self.buttons_label.pack(side=tkinter.LEFT)

    def create_axis(self):
        """Creates the x and y axis"""
        self.axis.set(xlim=self.xlim, ylim=self.ylim)
        self.axis.grid(True)
        self.axis.spines["left"].set_position("zero")
        self.axis.spines["bottom"].set_position("zero")
        self.axis.spines["right"].set_color("none")
        self.axis.spines["top"].set_color("none")
        self.axis.xaxis.set_ticks_position("both")
        self.axis.yaxis.set_ticks_position("both")

    def switch_line_style(self, n):
        if self.line_styles[n] == "-":
            self.line_styles[n] = "None"
        elif self.line_styles[n] == "None":
            self.line_styles[n] = "-"

        self.xlim = self.axis.get_xlim()  # get current zoom levels
        self.ylim = self.axis.get_ylim()
        self.redraw_all()

    def redraw_all(self):
        self.axis.clear()
        self.create_axis()
        if self.f.function != "0" and self.f.function != "":
            if self.line_styles[0] == "-":
                self.axis.plot(self.f.x_values, self.f.y_values, self.line_styles[0], label="f(x)", color="b")
            else:
                self.axis.plot(self.f.x_values, self.f.y_values, self.line_styles[0], label="f(x)")

            if self.d1.function != "0":
                if self.line_styles[1] == "-":
                    self.axis.plot(self.d1.x_values, self.d1.y_values, self.line_styles[1], label="f'(x)", color="r")
                else:
                    self.axis.plot(self.d1.x_values, self.d1.y_values, self.line_styles[1], label="f'(x)")
                if self.d2.function != "0":
                    if self.line_styles[2] == "-":
                        self.axis.plot(self.d2.x_values, self.d2.y_values, self.line_styles[2], label="f''(x)", color="y")
                    else:
                        self.axis.plot(self.d2.x_values, self.d2.y_values, self.line_styles[2], label="f''(x)")
                    if self.d3.function != "0":
                        if self.line_styles[3] == "-":
                            self.axis.plot(self.d3.x_values, self.d3.y_values, self.line_styles[3], label="f'''(x)", color="m")
                        else:
                            self.axis.plot(self.d3.x_values, self.d3.y_values, self.line_styles[3], label="f'''(x)")
        self.axis.legend(loc='lower left')
        self.canvas.draw()

    def reset_graph(self):
        self.xlim = (-4.1, 4.1)  # default x-left, x-right
        self.ylim = (-4.1, 4.1)  # default y-down, y-up
        self.line_styles = ["-", "-", "None", "None"]
        self.axis.clear()
        self.create_axis()
        self.canvas.draw()
        self.button_fx.destroy()
        self.button_dx_1.destroy()
        self.button_dx_2.destroy()
        self.button_dx_3.destroy()
        self.buttons_label.destroy()

if __name__ == "__main__":
    from function_module import Function as function
    from function_module import MainFunction as main_function
    root = tkinter.Tk()

    f_test = main_function("x^6 - x^4")
    d1_test = function("6*x^5 - 4*x^3")
    d2_test = function("30*x^4 - 12*x^2")
    d3_test = function("120*x^3 - 24*x")

    graph = Graph(root, f_test, d1_test, d2_test, d3_test)
    graph.pack()

    graph.redraw_all()
    graph.create_function_buttons()

    root.mainloop()