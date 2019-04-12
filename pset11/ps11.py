# coding: utf-8
# Problem Set 11: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import ps11_visualize
import matplotlib.pyplot as plt

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real number indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        # self.total = [[0]*width]*height
        self.tiles = width * height
        self.width = width
        self.height = height
        self.total = []
        for w in range(width):
            tmp = []
            for h in range(height):
                tmp.append(0)
            self.total.append(tmp)

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        width = int(math.floor(pos.getX()))
        height = int(math.floor(pos.getY()))
        # print pos.getX(), pos.getY(), width, height
        self.total[width][height] = 1

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.total[m][n] == 1

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.tiles

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        sum_ = 0
        for w in xrange(self.width):
            for h in xrange(self.height):
                sum_ += self.total[w][h]
        return sum_

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        width = random.random()*self.width
        height = random.random()*self.height
        return Position(width, height)

    def isPositionInRoom(self, pos):
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        if self.width > pos.getX() > 0 and self.height > pos.getY() >= 0:
            return True
        return False

class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.d = random.randint(0, 360-1)
        self.a = room.getRandomPosition()

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.a

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.a = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction

class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos = self.getRobotPosition()
        while True:
            new_pos = pos.getNewPosition(self.d, self.speed)
            if self.room.isPositionInRoom(new_pos):
                self.room.cleanTileAtPosition(new_pos)
                self.setRobotPosition(new_pos)
                break
            else:
                self.d = random.randint(0, 360 - 1)  # new direction


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    anim = 0
    if visualize:
        anim = ps11_visualize.RobotVisualization(num_robots, width, height)
    room = RectangularRoom(width, height)

    robots = []
    for robo in xrange(num_robots):
        robot = robot_type(room, speed)
        robots.append(robot)

    result_code = []
    for time in xrange(num_trials):
        for robot in robots:
            robot.updatePositionAndClean()

        if visualize:
            anim.update(room, robots)

        totalTile = room.getNumTiles()
        cleanedTile = room.getNumCleanedTiles()
        percent = cleanedTile/1.0/totalTile
        result_code.append(percent)
        if percent > min_coverage:
            break

    if visualize:
        anim.done()

    return result_code

def testSimulation():
    runSimulation(10, 1.2, 10, 15, 0.8, 40, Robot, True)

# testSimulation()

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    num_trails = 700
    result5 = runSimulation(1, 1.0, 5, 5, 0.75, num_trails, Robot, False)
    result10 = runSimulation(1, 1.0, 10, 10, 0.75, num_trails, Robot, False)
    result15 = runSimulation(1, 1.0, 15, 15, 0.75, num_trails, Robot, False)
    result20 = runSimulation(1, 1.0, 20, 20, 0.75, num_trails, Robot, False)
    result25 = runSimulation(1, 1.0, 25, 25, 0.75, num_trails, Robot, False)

    name_list = ['5*5', '10*10', '15*15', '20*20', '25*25']
    num_list = [len(result5), len(result10), len(result15), len(result20), len(result25)]
    plt.bar(range(len(num_list)), num_list, tick_label=name_list)
    plt.title('1. time VS. room size')
    plt.ylabel('cleaning time')
    plt.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    # fig, ax = plt.subplot()
    num_trails = 1000
    clean_time = []
    for single_b in range(11):
        result = runSimulation(single_b, 1.0, 25, 25, 0.75, num_trails, Robot, False)
        clean_time.append(len(result))
    plt.plot(range(11), clean_time, '-o')
    plt.show()


def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    num_trails = 1000
    result1 = runSimulation(1, 1.0, 20, 20, 0.75, num_trails, Robot, False)
    result2 = runSimulation(1, 1.0, 25, 16, 0.75, num_trails, Robot, False)
    result3 = runSimulation(1, 1.0, 40, 10, 0.75, num_trails, Robot, False)
    result4 = runSimulation(1, 1.0, 50, 8, 0.75, num_trails, Robot, False)
    result5 = runSimulation(1, 1.0, 80, 5, 0.75, num_trails, Robot, False)
    name_list = ['20/20', '25*16', '40*10', '50*8', '80*5']
    num_list = [len(result1), len(result2), len(result3), len(result4), len(result5)]
    plt.bar(range(len(num_list)), num_list, tick_label=name_list)
    plt.show()


def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    percent_list = []
    for i in range(0, 10):
        percent_list.append(i*0.1)

    legeng_name = []
    num_trails = 2000
    for robot_num in range(1, 6):
        result_curve = []
        for cover in percent_list:
            result1 = runSimulation(robot_num, 1.0, 25, 25, 0.75, num_trails, Robot, False)
            result_curve.append(len(result1))
        plt.plot(percent_list, result_curve, '-o')
        legeng_name.append('robot_num %d' % robot_num)
    plt.legend(tuple(legeng_name))
    plt.show()


# showPlot1()
# showPlot2()
# showPlot3()
# showPlot4()

# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        pos = self.getRobotPosition()
        self.d = random.randint(0, 360 - 1)  # new direction
        while True:
            new_pos = pos.getNewPosition(self.d, self.speed)
            if self.room.isPositionInRoom(new_pos):
                self.room.cleanTileAtPosition(new_pos)
                self.setRobotPosition(new_pos)
                break
            else:
                self.d = random.randint(0, 360 - 1)  # new direction

def testRandomWalkRobot():
    runSimulation(10, 1.2, 10, 15, 0.8, 40, RandomWalkRobot, True)

# testRandomWalkRobot()


# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    #  主要依据：清理能能力——不同数量、面积（规模）、不同覆盖率、不同速度
    num_trails = 3000
    robot_type = [Robot, RandomWalkRobot]

    legend_list = []
    for robot_ in robot_type:
        clean_time = []
        for single_b in range(1, 6):
            result = runSimulation(single_b, 1.0, 25, 25, 0.75, num_trails, robot_, False)
            clean_time.append(len(result))
        if robot_ == Robot:
            legend_list.append('Robot')
        else:
            legend_list.append('RandomWalkRobot')
        plt.plot(range(1, 6), clean_time, '-o')
    plt.legend(legend_list)
    plt.show()

showPlot5()

# total cost about 3 hours

