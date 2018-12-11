# A color-based tracker for grids

This is part of a university project. It consisted in creating a physical game of "labyrinth". 
A mechanical table, supported by 4 engines given it 4 degrees of freedom was given to hold a dockable 
model of a labyrinth. A camera sits on top of the layout, capturing the movements of a small ball, whose
goal is to move from position "1,1" to  position "7,7" in the labyrinth, avoiding red squares and 
passing through the biggest number of green squares possible.

The camera's (and therefore this algorithm's) job is to track the position of the ball on a 7x7 grid, 
and send that position to an Arduino which controls the table and displays results. 
It achieves that task by filtering all non-black (above 50 in RGB in any channel) values. 
It then choses the center of the biggest black cluster. 
The position is then discretized into a square grid that is shown on the image for reference.

You may freely reproduce this algorithm given you cite this page.



A video of the project can be found on: https://www.youtube.com/watch?v=3PzSuMU1TCA

## 
