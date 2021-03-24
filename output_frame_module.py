# coding=utf-8
import Tkinter as tkinter

from function_module import Function as function
from function_module import MainFunction as main_function
from function_operations_module import Methods as function_operations
from top_window_module import TangentAndNormalWindow as tangent_normal_window


class OutputFrame(tkinter.Frame):
    """Frame with drop-down menu which cycles through different results"""
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent, width=500, height=600, bg="white")  # super
        self.pack_propagate(False)

        self.option = tkinter.StringVar(parent)
        self.option.set("Option auswählen") # initial value

        self.dropdown_menu = tkinter.OptionMenu(self, self.option,
                                           "1. Ableitungen",
                                           "2. Achsenschnittpunkte",
                                           "3. Extrempunkte",
                                           "4. Wendepunkte, Sattelpunkte, Wendetangente",
                                           "5. Tangente und Normale in einem Punkt")
        self.dropdown_menu.pack()
        self.dropdown_menu.configure(width=60, state="disabled")  # defaults as frozen

        self.text = ""
        self.message = tkinter.Message(self, font=("Segoe", 14, "normal"), text="", bg="white", width=450)
        self.message.pack()

    def create_pages(self, f, d1, d2, d3):
        # region Page 1. Ableitungen
        self.page_1_text = "\n\n\n"
        if f.function != "0":
            self.page_1_text += "f(x) = " + function_operations.convert_from_sp(f.function)\
                                + "\n\n"
        if d1.function != "0":
            self.page_1_text += "f'(x) = " + function_operations.convert_from_sp(d1.function)\
                                + "\n\n"
        if d2.function != "0":
            self.page_1_text += "f''(x) = " + function_operations.convert_from_sp(d2.function)\
                                + "\n\n"
        if d3.function != "0":
            self.page_1_text += "f'''(x) = " + function_operations.convert_from_sp(d3.function)\
                                + "\n\n"
        # endregion

        # region Page 2. Achsenschnittpunkte
        self.page_2_text = "\n\n\n"
        if len(f.point_y_0) == 1:
            self.page_2_text += "f(x) schneidet die y-Achse an der Stelle:  "
            for point in f.point_y_0:
                self.page_2_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        else:
            self.page_2_text += "f(x) schneidet die y-Achse nicht.\n\n"

        if len(f.points_x_0) == 1:
            self.page_2_text += "f(x) schneidet die x-Achse an der Stelle:\n"
            for point in f.points_x_0:
                self.page_2_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(f.points_x_0) == 0:
            self.page_2_text += "f(x) schneidet die x-Achse nicht.\n\n"
        elif len(f.points_x_0) > 1:
            self.page_2_text += "f(x) schneidet die x-Achse an den Stellen:\n"
            for point in f.points_x_0:
                self.page_2_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n"
        # endregion

        # region Page 3. Extrempunkte
        self.page_3_text = "\n\n\n"
        if len(f.min_points) == 1:
            self.page_3_text += "f(x) hat den Tiefpunkt:\n"
            for point in f.min_points:
                self.page_3_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(f.min_points) == 0:
            self.page_3_text += "f(x) hat keine Tiefpunkte.\n\n"
        elif len(f.min_points) > 1:
            self.page_3_text += "f(x) hat folgende Tiefpunkte:\n"
            for point in f.min_points:
                self.page_3_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n"
            self.page_3_text += "\n\n"

        if len(f.max_points) == 1:
            self.page_3_text += "f(x) hat den Hochpunkt:\n"
            for point in f.max_points:
                self.page_3_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(f.max_points) == 0:
            self.page_3_text += "f(x) hat keine Hochpunkte.\n\n"
        elif len(f.max_points) > 1:
            self.page_3_text += "f(x) hat folgende Hochpunkte:\n"
            for point in f.max_points:
                self.page_3_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n"
        # endregion

        # region Page 4. Wendepunkte

        self.page_4_text = "\n\n\n"
        # add turning points
        if len(f.turning_points) == 1:
            self.page_4_text += "f(x) hat den Wendepunkt:  "
            for point in f.turning_points:
                self.page_4_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(f.turning_points) == 0:
            self.page_4_text += "f(x) hat keine Wendepunkte.\n\n"
        elif len(f.turning_points) > 1:
            self.page_4_text += "f(x) hat folgende Wendepunkte:\n"
            for point in f.turning_points:
                self.page_4_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n"
            self.page_4_text += "\n\n"

        # add saddle points
        if len(f.saddle_points) == 1:
            self.page_4_text += "f(x) hat den Sattelpunkt:  "
            for point in f.saddle_points:
                self.page_4_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n\n"
        elif len(f.saddle_points) == 0:
            self.page_4_text += "f(x) hat keine Sattelpunkte.\n\n"
        elif len(f.saddle_points) > 1:
            self.page_4_text += "f(x) hat folgende Sattelpunkte:\n  "
            for point in f.saddle_points:
                self.page_4_text += "(" + str(point[0]) + " | " + str(point[1]) + ")\n"
            self.page_4_text += "\n\n"

        # add turning tangents
        self.page_4_text += "\n\n"
        if len(f.turning_tangents) == 0:
            self.page_4_text += "f(x) hat keine Wendetangenten."
        elif len(f.turning_points) == len(f.turning_tangents):
            self.page_4_text += "Wendetangente:\n\n"
            for counter, point in enumerate(f.turning_points):
                self.page_4_text += "t(x) = " + f.turning_tangents[counter] + "    in (" + \
                                    str(point[0]) + " | " + str(point[1]) + ")\n"

        # endregion

    def update_page(self, f, d1):
        tangent_normal_window.destroy_all_toplevels(root)
        if self.option.get() == "1. Ableitungen":
            self.text = self.page_1_text
            self.message.configure(text=self.text)
        elif self.option.get() == "2. Achsenschnittpunkte":
            self.text = self.page_2_text
            self.message.configure(text=self.text)
        elif self.option.get() == "3. Extrempunkte":
            self.text = self.page_3_text
            self.message.configure(text=self.text)
        elif self.option.get() == "4. Wendepunkte, Sattelpunkte, Wendetangente":
            self.text = self.page_4_text
            self.message.configure(text=self.text)
        elif self.option.get() == "5. Tangente und Normale in einem Punkt":
            tangent_normal_window(root, f, d1)

    def clear(self):
        self.option.set("Option auswählen")  # initial value
        self.dropdown_menu.configure(state="disabled")

        self.text = ""
        self.message.configure(text="")

    @staticmethod
    def destroy_all_toplevels(window):
        """Destroys all widgets of window that are Toplevel"""
        for widget in window.winfo_children():
            if isinstance(widget, tkinter.Toplevel):
                widget.destroy()


if __name__ == "__main__":
    root = tkinter.Tk()

    f_test = main_function("x^6 - x^4")
    d1_test = function("6*x^5 - 4*x^3")
    d2_test = function("30*x^4 - 12*x^2")
    d3_test = function("120*x^3 - 24*x")

    f_test.point_y_0 = function_operations.find_point_y_0(f_test.function)
    for value in function_operations.find_points_x_0(f_test.function):
        f_test.points_x_0.append((value, 0))

    f_test.min_points = function_operations.find_min_points(f_test.function, d1_test.function, d2_test.function)

    f_test.max_points = function_operations.find_max_points(f_test.function, d1_test.function, d2_test.function)

    f_test.turning_points = function_operations.find_turning_points(f_test.function, d2_test.function,
                                                                           d3_test.function)

    f_test.turning_tangents = function_operations.find_turning_tangents(f_test.turning_points, d1_test.function)

    f_test.saddle_points = function_operations.find_saddle_points(f_test.function, d1_test.function,
                                                                         f_test.turning_points)

    output_frame = OutputFrame(root)
    output_frame.pack()

    output_frame.create_pages(f_test, d1_test, d2_test, d3_test)

    # callback to the dropdown menu
    output_frame.option.trace("w", lambda *args: output_frame.update_page(f_test.function, d1_test.function))
    output_frame.dropdown_menu.configure(width=60, state="normal")

    root.mainloop()