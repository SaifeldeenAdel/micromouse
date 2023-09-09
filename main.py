from Maze import Maze
from Mouse import Mouse
from DIRECTIONS import Directions
import myAPI

###############################
### Still very incomplete.  ###
###############################


def main():
  maze = Maze(16, 16)
  mouse = Mouse(0, 0, Directions.NORTH)

  while True: 
    updateWalls(maze,mouse)
    mouse.moveForward()


def updateWalls(maze: Maze, mouse: Mouse) -> None:
    """Updates walls in maze data"""
    if myAPI.wallFront():
        maze.setWall(mouse.getPosition, mouse.getDirection)
        print("WALL FRONT")
    if myAPI.wallLeft():
        maze.setWall(mouse.getPosition, mouse.getDirection)
        print("WALL LEFT")
    if myAPI.wallRight():
        maze.setWall(mouse.getPosition, mouse.getDirection)
        print("WALL RIGHT")
        
        
        
        
# Main Algorithm function, tested only on simulator
def updateFlood(maze: Maze, mouse: Mouse, flag: str) -> None:
    """Updates flood array values, runs flood fill algorithm"""

    # Flood fill algorithm based on if its the center run or home run
    if flag is "center":
        maze.clearFlood("center")
        # Queue starts with all 4 center cells
        queue = [center for center in maze.getCenters()]

        while len(queue) != 0:
            current = queue.pop(0)
            # Goes through all accessible neighbors and updates flood values if they aren't center cells or don't already have a value
            for neighbor in maze.getAccessibleNeighbors(current):
                if (
                    not maze.isInCenter(neighbor)
                    and (neighbor not in queue)
                    and (not maze.isFlooded(neighbor))
                ):
                    maze.flowFlood(current, neighbor)
                    queue.append(neighbor)

    elif flag is "home":
        maze.clearFlood("home")
        # Queue starts with home cell
        queue = [(0, 0)]

        while len(queue) != 0:
            current = queue.pop(0)
            for neighbor in maze.getAccessibleNeighbors(current):
                if (neighbor not in queue) and (not maze.isFlooded(neighbor)):
                    maze.flowFlood(current, neighbor)
                    queue.append(neighbor)




if __name__ == "__main__":
    main()



