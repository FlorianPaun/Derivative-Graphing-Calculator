# coding=utf-8
import Tkinter as tkinter
import output_frame_module

from function_module import Function as function
from function_module import MainFunction as main_function
from function_operations_module import Methods as function_operations
from keyboard_frame_module import Keyboard as keyboard
from output_frame_module import OutputFrame as output
from graph_frame_module import Graph as graph


def start():
    if frame_keyboard.function == "":
        return
    if frame_keyboard.openBracketsCounter == frame_keyboard.closedBracketsCounter and frame_keyboard.function != "":
        try:
            welcome_frame.destroy()
        except:
            pass

        if frame_keyboard.function[-1] in "*^-+.":
            frame_keyboard.function = frame_keyboard.function[:-1]
            frame_keyboard.labelFunction.configure(text=frame_keyboard.function)

        frame_keyboard.freeze_buttons()

        # first create the 4 functions
        fx = main_function(function_operations.convert_to_sp(frame_keyboard.function))
        dx_1 = function(function_operations.derive_function(fx.function))
        dx_2 = function(function_operations.derive_function(dx_1.function))
        dx_3 = function(function_operations.derive_function(dx_2.function))


        # calculate all important points of f(x)
        fx.point_y_0 = function_operations.find_point_y_0(fx.function)
        for value in function_operations.find_points_x_0(fx.function):
            fx.points_x_0.append((value, 0))
        fx.min_points = function_operations.find_min_points(fx.function, dx_1.function, dx_2.function)
        fx.max_points = function_operations.find_max_points(fx.function, dx_1.function, dx_2.function)
        fx.turning_points = function_operations.find_turning_points(fx.function, dx_2.function, dx_3.function)
        fx.turning_tangents = function_operations.find_turning_tangents(fx.turning_points, dx_1.function)
        fx.saddle_points = function_operations.find_saddle_points(fx.function, dx_1.function, fx.turning_points)


        # create and configure the output frame
        frame_output = output(root)

        # callback to the drop-down menu:
        frame_output.option.trace("w", lambda *args: frame_output.update_page(fx.function, dx_1.function))

        output_frame_module.root = root  # passing the parent window of main to the module
        frame_output.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        frame_output.create_pages(fx, dx_1, dx_2, dx_3)
        frame_output.dropdown_menu.configure(state="normal")


        # create and configure the graph frame
        frame_graph = graph(root, fx, dx_1, dx_2, dx_3)
        frame_graph.pack(side=tkinter.LEFT, anchor=tkinter.NW)
        frame_graph.redraw_all()
        frame_graph.create_function_buttons()

def reset():
    frame_keyboard.unfreeze_buttons()
    frame_keyboard.function = ""
    frame_keyboard.openBracketsCounter = 0
    frame_keyboard.closedBracketsCounter = 0
    frame_keyboard.labelFunction.configure(text="")

    for widget in root.winfo_children():
        if isinstance(widget, (graph, output, tkinter.Toplevel)):
            widget.destroy()
    frame_keyboard.function = ""
    frame_keyboard.labelFunction.config(text="")


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Kurvendiskussion")
    root.config(bg="white")
    root.geometry("1400x700")
    root.resizable(False, False)

    frame_keyboard = keyboard(root)
    frame_keyboard.pack(side=tkinter.LEFT, anchor=tkinter.NW)
    frame_keyboard.start = start  # passing the start function from main to the keyboard module
    frame_keyboard.reset = reset  # passing the reset function from main to the keyboard module

    welcome_frame = tkinter.Frame(root, bg="white", width=1100, height=700)
    welcome_frame.pack_propagate(False)
    welcome_frame.pack(side=tkinter.LEFT, anchor=tkinter.NW)

    welcome_message = tkinter.Message(welcome_frame, text="""\n\n
    Geben Sie links eine Funktion ein und das Programm berechnet für Sie:\n
    - die ersten drei Ableitungen der Funktion
    - die Schnittpunkte mit den Achsen
    - die Extrempunkte
    - die Wendepunkte und ihre Tangenten
    - die Sattelpunkte
    - eine interaktive graphische Darstellung der Funktion und ihrer Ableitungen\n\n\n
    
    Zusätzlich können Sie auch die Koordinaten eines Punktes eingeben und das Programm 
    sagt Ihnen ob der Punkt auf dem Graph der Funktion liegt und wenn ja, die Gleichungen 
    der Tangente und der Normale, die durch den Punkt verlaufen.""",
                                      font=("Segoe", 18, "normal"), bg="white", width=1000)
    welcome_message.pack()

    root.mainloop()
