# 6.00 Problem Set 9
#
# Name:
# Collaborators:
# Time:

from string import *
import math

IMPORT_FILE_NAME = 'shapes.txt'

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")

class Square(Shape):
    def __init__(self, h):
        """
        h: length of side of the square
        """
        self.side = float(h)
    def area(self):
        """
        Returns area of the square
        """
        return self.side**2
    def __str__(self):
        return 'Square with side ' + str(self.side)
    def __eq__(self, other):
        """
        Two squares are equal if they have the same dimension.
        other: object to check for equality
        """
        return type(other) == Square and self.side == other.side

class Circle(Shape):
    def __init__(self, radius):
        """
        radius: radius of the circle
        """
        self.radius = float(radius)
    def area(self):
        """
        Returns approximate area of the circle
        """
        return 3.14159*(self.radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self.radius)
    def __eq__(self, other):
        """
        Two circles are equal if they have the same radius.
        other: object to check for equality
        """
        return type(other) == Circle and self.radius == other.radius

#
# Problem 1: Create the Triangle class
#
## TO DO: Implement the `Triangle` class, which also extends `Shape`.
class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return self.base*self.height/2.0

    def __str__(self):
        return "Triangle with base %s and height %s." % (self.base, self.height)

    def __eq__(self, other):
        return type(other) == Triangle and self.base == other.base and self.height == other.height
#
# Problem 2: Create the ShapeSet class
#
## TO DO: Fill in the following code skeleton according to the
##    specifications.

class ShapeSet:
    def __init__(self):
        """
        Initialize any needed variables
        """
        ## TO DO
        self.shapes = []
        self.index_ = -1

    def addShape(self, sh):
        """
        Add shape sh to the set; no two shapes in the set may be
        identical
        sh: shape to be added
        """
        ## TO DO
        self.shapes.append(sh)
        self.index_ = -1

    def __iter__(self):
        """
        Return an iterator that allows you to iterate over the set of
        shapes, one shape at a time
        """
        ## TO DO
        for shape in self.shapes:
            yield shape

    def __str__(self):
        """
        Return the string representation for a set, which consists of
        the string representation of each shape, categorized by type
        (circles, then squares, then triangles)
        """
        ## TO DO
        str_out = ''
        for shape in self.shapes:
            if type(shape) == Square:
                str_out += str(shape) + ' \n'

        for shape in self.shapes:
            if type(shape) == Circle:
                str_out += str(shape) + ' \n'

        for shape in self.shapes:
            if type(shape) == Triangle:
                str_out += str(shape) + ' \n'
        return str_out
        
#
# Problem 3: Find the largest shapes in a ShapeSet
#
def findLargest(shapes):
    """
    Returns a tuple containing the elements of ShapeSet with the
       largest area.
    shapes: ShapeSet
    """
    max_area = 0
    for idx, shape in enumerate(shapes):
        if shape.area() > max_area:
            max_area = shape.area()

    result = []
    for idx, shape in enumerate(shapes):
        if shape.area() == max_area:
            result.append(shape)
    return tuple(result)

#
# Problem 4: Read shapes from a file into a ShapeSet
#
def readShapesFromFile(filename):
    """
    Retrieves shape information from the given file.
    Creates and returns a ShapeSet with the shapes found.
    filename: string
    """
    ## TO DO
    ss = ShapeSet()
    for str_line in open(filename):
        str_list = str_line.split(',')
        # print float(str_list[1])
        if str_list[0] == 'circle':
            ss.addShape(Circle(float(str_list[1])))
        elif str_list[0] == 'square':
            ss.addShape(Square(float(str_list[1])))
        elif str_list[0] == 'triangle':
            ss.addShape(Triangle(float(str_list[1]), float(str_list[2])))
    return ss


def testA():
    ss = ShapeSet()
    ss.addShape(Triangle(1.2, 2.5))
    ss.addShape(Circle(4))
    ss.addShape(Square(3.6))
    ss.addShape(Triangle(1.6, 6.4))
    ss.addShape(Circle(2.2))
    largest = findLargest(ss)
    largest
    for e in largest:
        print e

# testA()

def testB():
    ss = readShapesFromFile(IMPORT_FILE_NAME)
    print ss

testB()

