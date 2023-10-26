# import os
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.pyplot import rcParams
import convert_img


filename='path/cspace'
# convert_img.convert_imgage(filename)


class TreeNode():
    def __init__(self, locationX, locationY):
        self.locationX=locationX        ## X Location
        self.locationY=locationY        ## Y Location
        self.children=[]                ## Children List
        self.parent=None                ## Parent node


class RRTAlgorithm():
    def __init__(self, start, goal, numIterations, grid, stepSize):
        self.randomTree=TreeNode(start[0], start[1])
        self.goal=TreeNode(goal[0], goal[1])
        self.nearestNode=None
        self.interations=min(numIterations, 500)    ## # of iterations to run
        self.grid=grid                              ## map
        self.stepSize=stepSize                      ## length of each branch
        self.pathDist=0                             ## total path distance
        self.nearestDist=10000                      ## distance to nearest node
        self.numWayPoints=0
        self.wayPoints=[]


    def addChild(self, locationX, locationY):
        ## Add the point to the nearest node and add goal when reached
        if (locationX == self.goal.locationX):
            self.nearestNode.children.append(self.goal)
            self.goal.parent=self.nearestNode
        else:
            tempNode=TreeNode(locationX, locationY)
            self.nearestNode.children.append(tempNode)
            tempNode.parent=self.nearestNode


    def sampleAPoint(self):
        ## Sample a random point within grid lmits
        x=random.randint(1, grid.shape[1])
        y=random.randint(1, grid.shape[0])
        point = np.array([x, y])

        return point


    def steerToPoint(self, locationStart, locationEnd):
        ## Steer a distance stepsize from start to end location
        offset=(self.stepSize)*(self.unitVector(locationStart, locationEnd))
        point=np.array([locationStart.locationX + offset[0], locationStart.locationY + offset[1]])

        if point[0] >= grid.shape[1]:
            point[0]=grid.shape[1]-1
        if point[1] >= grid.shape[0]:
            point[1]=grid.shape[0]-1

        return point


    def isInObstacle(self, locationStart, locationEnd):
        ## Check if obstacle lies between the start node and end point of the edge
        u_hat=self.unitVector(locationStart, locationEnd)
        testPoint=np.array([0.0, 0.0])
        
        for i in range(self.stepSize):
            testPoint[0]=locationStart.locationX + i*u_hat[0]
            testPoint[1]=locationStart.locationY + i*u_hat[1]

            if self.grid[round(testPoint[1]).astype(np.int64), round(testPoint[0]).astype(np.int64)]==1:
                return True
        return False


    def unitVector(self, locationStart, locationEnd):
        ## Find unit vector between 2 points which form a vector
        print("x: ", locationStart)
        v=np.array([locationEnd[0]-locationStart.locationX, locationEnd[1]-locationStart.locationY])
        # v=np.array([locationEnd.locationX - locationStart.locationX, locationEnd.locationY - locationStart.locationY])

        u_hat=v/np.linalg.norm(v)
        return u_hat
    

    def findNearest(self, root, point):
        ## Find the nearest node from a given unconnected point (Euclidean distance)
        if not root:
            return
        
        dist=self.distance(root, point)
        if dist <= self.nearestDist:
            self.nearestNode=root
            self.nearestDist=dist

        for child in root.children:
            self.findNearest(child, point)


    def distance(self, node1, point):
        ## Find euclidean distance between a node and an XY point
        dist=np.sqrt((node1.locationX-point[0])**2 + (node1.locationY-point[1])**2)
        return dist
    

    def goalFound(self, point):
        ## Check if the goal has been reached within step size
        if self.distance(self.goal, point) <= self.stepSize:
            return True


    def resetNearestValues(self):
        ## Reset nearestNode and nearest Distance
        self.nearestNode=None
        self.nearestNode=10000


    def retraceRRTPath(self, goal):
        ## Trace the path from goal to start
        if goal.locationX == self.randomTree.locationX:
            return
        
        self.numWayPoints += 1

        ## Insert currentPoint to the waypoints array from the beginning
        currentPoint=np.array([goal.locationX, goal.locationY])
        self.wayPoints.insert(0, currentPoint)
        self.pathDist += self.stepSize
        self.retraceRRTPath(goal.parent)


# def main():
grid=np.load(filename+'.npy')
start=np.array([250.0, 400.0])
goal=np.array([1250.0, 800.0])
numIterations=200
stepSize=50
goalRegion=plt.Circle((goal[0], goal[1]), stepSize, color='b', fill=False)

fig=plt.figure('RRT Algorithmm')
plt.imshow(grid, cmap='binary')
plt.plot(start[0], start[1], 'ro')        ## statPoint[0] is locationX, startPoint[1] is locationY
plt.plot(goal[0], goal[1], 'bo')
ax=fig.gca()
ax.add_patch(goalRegion)
plt.xlabel('X-axis $(m)$')
plt.ylabel('Y-axis $(m)$')
plt.show()

## Run the code
rrt = RRTAlgorithm(start, goal, numIterations, grid, stepSize)

for i in range(rrt.interations):
    ## Reset nearest value
    rrt.resetNearestValues()
    print("Iteration: ", i)

    ## Algorithm begin
    point=rrt.sampleAPoint()
    rrt.findNearest(rrt.randomTree, point)
    new=rrt.steerToPoint(rrt.nearestNode, point)

    bool=rrt.isInObstacle(rrt.nearestNode, new)

    if (bool == False):
        rrt.addChild(new[0], new[1])
        plt.pause(0.10)
        plt.plot([rrt.nearestNode.locationX, new[0]], [rrt.nearestNode.locationY, new[1]], 'go', linestyle="--")

        ## if goal found, append to path
        if (rrt.goalFound(new)):
            rrt.addChild(goal[0], goal[1])
            print("Goal Found!")
            break

## Trace back the path returned, and add start point to waypoints
rrt.retraceRRTPath(rrt.goal)
rrt.wayPoints.insert(0, start)
print("Number of waypoints: ", rrt.numWayPoints)
print("Path Distance (m): ", rrt.pathDist)
print("Waypoints: ", rrt.wayPoints)

# Plot waypoints
for i in range(len(rrt.wayPoints)-1):
    plt.plot([rrt.wayPoints[i][0], rrt.wayPoints[i+1][0]], [rrt.wayPoints[i][1], rrt.wayPoints[i+1][1]], 'ro', linestyle="--")
    plt.pause(0.10)


# if __name__ == '__main__':
#     main()