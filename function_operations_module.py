import sympy

from sympy.parsing.sympy_parser import parse_expr


class Methods:
    """Class of static methods, operations for working with functions"""

    @staticmethod
    def derive_function(f):
        """Returns the derivative of a function's expression, as a string"""
        d = str(sympy.diff(f))
        d = d.replace("exp", "E**")  # program can not work with exp(x), only e**x or e^x
        return d

    @staticmethod
    def convert_to_sp(f):
        """Converts some characters in the expression to characters that sympy can work with"""
        f = f.replace("^", "**")
        f = f.replace("e", "E")
        return f

    @staticmethod
    def convert_from_sp(f):
        """Converts some characters from the sympy namespace to characters that the user is used to seeing"""
        f = f.replace("**", "^")
        f = f.replace("E", "e")
        return f

    @staticmethod
    def find_point_y_0(function):
        """Returns the point (0, y)."""
        function = function.replace("x", "(0)")
        try:
            y_value = round(float(parse_expr(function)), 2)

            if y_value == int(y_value):  # in case of unnecessary float
                y_value = int(y_value)

            point = [(0, y_value)]
            return point
        except:
            return []

    @staticmethod
    def find_points_x_0(function):
        """Returns a list of x values by solving the equation f(x)=0 with sympy.solve"""
        try:
            function = sympy.simplify(function)  # convert from string to an actual expression
            x = sympy.Symbol("x")
            solutions = []

            for counter, value in enumerate(sympy.solve(function, x)):  # go through list of solutions for f(x) = 0
                # remove all non-float solutions
                try:
                    value = round(float(value), 2)
                    if value == int(value):  # remove unnecessary float like 0.0
                        solutions.append(int(value))
                    else:
                        solutions.append(value)
                except:
                    pass

            return solutions
        except:
            return []

    @staticmethod
    def find_min_points(f, d1, d2):
        """Returns a list of tuples (x, y), the point(s) where f(x) has minimum values"""
        try:
            # find the x values where f'(x) = 0
            x_values = Methods.find_points_x_0(d1)
            x_min_values = []

            for x_value in x_values:  # replace each x value in f''(x), in this case dx2
                expr = d2.replace("x", "(" + str(x_value) + ")")
                if parse_expr(expr) is not None:
                    if parse_expr(expr) > 0:  # f''(x) > 0 ==> min point, f''(x) < 0 ==> max point
                        x_min_values.append(x_value)

            # now put the x values from the previous step into f(x)to find the y values and complete the min points
            min_points = []
            for x_value in x_min_values:
                expr = f.replace("x", "(" + str(x_value) + ")")
                y_value = round(parse_expr(expr), 2)
                if y_value == int(y_value):  # remove unnecessary float like 0.0
                    min_points.append((x_value, int(y_value)))
                else:
                    min_points.append((x_value, y_value))

            return min_points
        except:
            return []

    @staticmethod
    def find_max_points(f, d1, d2):
        """Returns a list of tuples (x, y), the point(s) where f(x) has maximum values"""
        try:
            # find the x values where f'(x) = 0
            x_values = Methods.find_points_x_0(d1)
            x_max_values = []

            for x_value in x_values:  # replace each x value in f''(x), in this case dx2
                expr = d2.replace("x", "(" + str(x_value) + ")")
                if parse_expr(expr) is not None:
                    if parse_expr(expr) < 0:  # f''(x) > 0 ==> min point, f''(x) < 0 ==> max point
                        x_max_values.append(x_value)

            # now put the x values from the previous step into f(x)to find the y values and complete the min points
            max_points = []
            for x_value in x_max_values:
                expr = f.replace("x", "(" + str(x_value) + ")")
                y_value = round(parse_expr(expr), 2)
                if y_value == int(y_value):  # remove unnecessary float like 0.0
                    max_points.append((x_value, int(y_value)))
                else:
                    max_points.append((x_value, y_value))

            return max_points
        except:
            return []

    @staticmethod
    def find_turning_points(f, d2, d3):
        """Returns the turning points of f as a list of tuples (x, y)"""
        try:
            x_values = []
            turning_points = []

            # first find the solutions for f''(x)=0
            for counter, value in enumerate(Methods.find_points_x_0(d2)):  # go through list of solutions
                value = round(float(value), 2)
                if value == int(value):  # remove unnecessary float like 0.0
                    x_values.append(int(value))
                else:
                    x_values.append(value)

            for x_value in x_values:
                expr = d3.replace("x", "(" + str(x_value) + ")")
                if parse_expr(expr) != 0:  # if f'''(x) =/= 0 then it is a valid turning point
                    # now put the x value into f(x) to find the y value and complete the turning point
                    expr = f.replace("x", "(" + str(x_value) + ")")
                    y_value = round(parse_expr(expr), 2)
                    if y_value == int(y_value):  # remove unnecessary float like 0.0
                        turning_points.append((x_value, int(y_value)))
                    else:
                        turning_points.append((x_value, y_value))

            return turning_points
        except:
            return []

    @staticmethod
    def find_turning_tangents(turning_points, dx1):
        """Returns a list of strings expressions t(x)=mx+b"""
        try:
            turning_tangents = []
            for point in turning_points:
                # t(x) = m*x + b, m=f'(x)
                derivative = dx1.replace("x", str(point[0]))
                m = round(parse_expr(derivative), 2)
                if m == int(m):
                    m = int(m)
                b = round(point[1] - m * point[0], 2)  # b=y-m*x
                if b == int(b):
                    b = int(b)

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

                turning_tangents.append(tangent)
            return turning_tangents
        except:
            return []

    @staticmethod
    def find_saddle_points(f, d1, turning_points):
        """returns a list of points where f'(x) = 0 which are turning points as well"""
        try:
            possible_saddle_points = []
            saddle_points = []
            for x_value in Methods.find_points_x_0(d1):
                expr = f.replace("x", "(" + str(x_value) + ")")
                y_value = round(parse_expr(expr), 2)
                if y_value == int(y_value):  # remove unnecessary float like 0.0
                    possible_saddle_points.append((x_value, int(y_value)))
                else:
                    possible_saddle_points.append((x_value, y_value))

            for point in possible_saddle_points:
                if point in turning_points:
                    saddle_points.append(point)

            return saddle_points
        except:
            return []


if __name__ == "__main__":
    f_test = "x**2"
