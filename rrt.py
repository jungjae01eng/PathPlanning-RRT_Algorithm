import os
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.pyplot import rcParams
import convert_img


'''
<Create the Configuration Space>
If you do not have a configuration space (maze), please place the PNG file in the 'path' folder and adjust the 'filename' variable accordingly.
'''

filename='path/cspace'
convert_img.convert_imgage(filename)


## TreeNoode Class
class TreeNode():
    def __init__(self, locationX, locationY):
        self.locationX=locationX        ## X Location
        self.locationY=locationY        ## Y Location
        self.children=[]                ## Children List
        self.parent=None                ## Parent node


## RRT Algorithm Class
class RRTAlgorithm():
    def __init__(self, start, goal, numIterations, grid, stepSize):
        self.randomTree=TreeNode(start[0], start[1])
        self.goal=TreeNode(goal[0], goal[1])
        self.nearestNode=None
        self.interations=numIterations              ## # of iterations to run
        self.grid=grid                              ## map
        self.stepSize=stepSize                      ## length of each branch
        self.pathDist=0                             ## total path distance
        self.nearestDist=10000                      ## distance to nearest node
        self.numWayPoints=0
        self.wayPoints=[]

    def addChild(self, locationX, locationY):
        ## Add the point to the nearest node and add goal when reached
        pass

    def sampleAPoint(self):
        ## Sample a random point within grid lmits
        pass

    def steerToPoint(self, locationStart, locationEnd):
        ## Steer a distance stepsize from start to end location
        pass

    def isInObstacle(self, locationStart, locationEnd):
        ## Check if obstacle lies between the start node and end point of the edge
        pass

    def unitVector(self, locationStart, locationEnd):
        ## Find unit vector between 2 points which form a vector
        pass

    def findNearest(self, root, point):
        ## Find the nearest node from a given unconnected point (Euclidean distance)

        pass

    def distance(self, node1, point):
        ## Find euclidean distance between a node and an XY point
        pass

    def goalFound(self, point):
        ## Check if the goal has been reached within step size
        pass

    def resetNearestValues(self):
        ## Reset nearestNode and nearest Distance
        pass

    def retraceRRTPath(self, goal):
        ## Trace the path from goal to start
        pass


def main():
    grid=np.load(filename+'.npy')
    startPoint=np.array([250.0, 400.0])
    goalPoint=np.array([1250.0, 800.0])
    numIterations=200
    stepSize=50
    goalRegion=plt.Circle((goalPoint[0], goalPoint[1]), stepSize, color='b', fill=False)

    fig=plt.figure('RRT Algorithmm')
    plt.imshow(grid, cmap='binary')
    plt.plot(startPoint[0], startPoint[1], 'ro')        ## statPoint[0] is locationX, startPoint[1] is locationY
    plt.plot(goalPoint[0], goalPoint[1], 'bo')
    ax=fig.gca()
    ax.add_patch(goalRegion)
    plt.xlabel('X-axis $(m)$')
    plt.ylabel('Y-axis $(m)$')
    plt.show()


if __name__ == '__main__':
    main()