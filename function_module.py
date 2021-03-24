import numpy
import sympy

sample_array_x_values = numpy.concatenate([numpy.arange(-10, -1.9, 0.2),
                                           numpy.arange(-1.95, 2.05, 0.05),
                                           numpy.arange(2.1, 10.1, 0.2)])  # denser values between -2 and 2

class Function:
    """A Function has an expression e.g. x^2+5, an array containing the X values (the same for all functions
    and an array containing the Y values. These are calculated by replacing each X value into the function's
    expression."""

    def __init__(self, expression):
        self.function = self.convert_to_sp(expression)

        self.x_values = sample_array_x_values.copy()

        self.y_values = self.calculate_y_values(self.function, self.x_values)

        self.remove_none_from_arrays()

    def reset(self):
        self.function = ""

    @staticmethod
    def convert_to_sp(f):
        """Converts some characters in the expression to characters that sympy can work with"""
        f = f.replace("^", "**")
        f = f.replace("e", "E")
        return f

    @staticmethod
    def calculate_y_values(f, x_values):
        """Calculates all y values by replacing x in the function's expression with every x value and parsing that
        using sympy.N()"""
        y_values = x_values.copy()
        for counter, value in enumerate(x_values):
            expr = f.replace("x", "(" + str(value) + ")")
            try:
                y_values[counter] = sympy.N(expr, 5)
            except:
                y_values[counter] = None
        return y_values

    def remove_none_from_arrays(self):
        """Removes all None objects from both arrays, because None cannot be drawn in the graph.
        e.g. x_values[3]=-2 and f(x)=sqrt(x)  ==>  y_values[3]=None
        x_values[3] and y_values[3] are removed."""

        is_nan = numpy.isnan(self.y_values)  # array of booleans, element is True if the corresponding element in
                                             # self.y_values is None

        self.x_values = self.x_values[numpy.logical_not(is_nan)]
        self.y_values = self.y_values[numpy.logical_not(is_nan)]  # replace all None elements


class MainFunction(Function):
    """A regular function for which all of the calculated values and points are stored."""
    def __init__(self, expression):
        Function.__init__(self, expression)  # super

        self.min_points = []
        self.max_points = []

        self.turning_points = []
        self.turning_tangents = []
        self.saddle_points = []

        self.point_y_0 = []
        self.points_x_0 = []

    def reset(self):
        self.function = ""
        self.min_points = []
        self.max_points = []
        self.turning_points = []
        self.turning_tangents = []
        self.saddle_points = []
        self.point_y_0 = []
        self.points_x_0 = []


if __name__ == "__main__":
    function = Function("x**E")
