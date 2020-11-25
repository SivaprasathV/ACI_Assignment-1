# Importing libraries
from copy import deepcopy


class blocks:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.parent_action = None
        self.position = position
        if position[0] < position[2] or position[1] < position[3]:
            self.head, self.tail = (position[0], position[1]), (position[2], position[3])
        else:
            self.head, self.tail = (position[2], position[3]), (position[0], position[1])
        self.g = self.h = 0

    @property
    def f(self):
        return self.g + self.h

    @property
    def align(self):
        return 'Standing' if self.head == self.tail else 'Lying Horizontal' if self.head[0] == self.tail[
            0] else 'Lying Vertical'


def a_star_search(_map, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given terrain"""

    # checking for goal
    if end is None:
        for xi in _map:
            for xj in xi:
                if xj == 9:
                    Gx_ = _map.index(xi)
                    Gy_ = xi.index(xj)
                    end = (Gx_, Gy_, Gx_, Gy_)

    # Create start and end node
    final_path = []
    startBlock = blocks(None, start)
    goal = blocks(None, end)
    startBlock.h = abs(startBlock.tail[0] - goal.position[0]) + abs(startBlock.tail[1] - goal.position[1])

    # Initialize both open and closed list
    openList = []
    closedList = []

    # Add the start node
    openList.append(startBlock)

    # Loop until you find the end
    while len(openList) > 0:
        curBlock = openList[0]

        for b in openList:
            curBlock = (b if b.f < curBlock.f else curBlock)

        # Pop current off open list, add to closed list
        openList.pop(openList.index(curBlock))
        closedList.append(curBlock)

        # If Goal is found
        if curBlock.position == goal.position:
            traversal = []
            cur = curBlock
            while cur is not None:
                traversal.append([cur.position, cur.parent_action])
                cur = cur.parent
            traversal.reverse()

            # Getting the final path
            final_path = traversal
            break

        # Generating Child Nodes
        childrenBlocks = []
        new_pos_list = None
        x1, y1, x2, y2 = curBlock.position
        if curBlock.align == 'Standing':
            new_pos_list = [(x1, y1 + 1, x2, y2 + 2, 'R'), (x1, y1 - 2, x2, y2 - 1, 'L'), (x1 - 2, y1, x2 - 1, y2, 'U'),
                            (x1 + 1, y1, x2 + 2, y2, 'D')]
        if curBlock.align == 'Lying Horizontal':
            new_pos_list = [(x1, y1 + 2, x2, y2 + 1, 'R'), (x1, y1 - 1, x2, y2 - 2, 'L'), (x1 - 1, y1, x2 - 1, y2, 'U'),
                            (x1 + 1, y1, x2 + 1, y2, 'D')]
        if curBlock.align == 'Lying Vertical':
            new_pos_list = [(x1, y1 + 1, x2, y2 + 1, 'R'), (x1, y1 - 1, x2, y2 - 1, 'L'), (x1 - 1, y1, x2 - 2, y2, 'U'),
                            (x1 + 2, y1, x2 + 1, y2, 'D')]

        for p in new_pos_list:
            # Make sure within range
            if p[0] > (len(_map) - 1) or p[0] < 0 or p[1] > (len(_map[0]) - 1) or p[1] < 0 \
                    or p[2] > (len(_map) - 1) or p[2] < 0 or p[3] > (len(_map[0]) - 1) or p[3] < 0:
                continue

            # Make sure walkable terrain
            if _map[p[0]][p[1]] < 1 or _map[p[2]][p[3]] < 1:
                continue

            # Create new node
            newBlock = blocks(curBlock, p[:4])
            newBlock.g = curBlock.g + 1
            newBlock.h = abs(newBlock.tail[0] - goal.position[0]) + abs(newBlock.tail[1] - goal.position[1])
            newBlock.parent_action = p[4]

            if newBlock.h > curBlock.h:
                continue
            # Append
            childrenBlocks.append(newBlock)

        # Loop through children
        for childB in childrenBlocks:
            # if Child is on the closed list
            for cB in closedList:
                if childB.position == cB.position:
                    continue
            # Assigning g(n) and h(n) values
            childB.g = curBlock.g + 1
            childB.h = abs(curBlock.tail[0] - goal.position[0]) + abs(curBlock.tail[1] - goal.position[1])

            # if Child already in open list
            for oB in openList:
                if childB == oB and childB.g > oB.g:
                    continue
                if childB.f > oB.f:
                    continue

            # Add child to Open list
            openList.append(childB)

    # Return the final Path of traversal
    return final_path


def solve_map(m, s, g=None):
    # function to print the results

    # calling the A star algorithm implementaion
    path_Astar = a_star_search(m, s, g)
    step_count = len(path_Astar)-1
    print(
        f'The A Star search Algorithm provided a solution with {step_count} \n =======================================')
    for sc, sm in enumerate(path_Astar):
        move_map = deepcopy(m)
        if sm[1] == 'R':
            move_1 = 'Right'
        elif sm[1] == 'L':
            move_1 = 'Left'
        elif sm[1] == 'U':
            move_1 = 'Up'
        elif sm[1] == 'D':
            move_1 = 'Down'
        else:
            move_1 = 'Start'

        print(f'Step {sc} : {move_1}\n')
        Ax_, Ay_, Bx_, By_ = sm[0]

        # Applying the moves on to the map
        move_map[Ax_][Ay_] = move_map[Bx_][By_] = 'X'

        # Replacing 1, 0 , X and 9 with unicode characters for printing
        for mm in move_map:
            plist = []
            for mm2 in mm:
                if mm2 == 1:
                    plist.append('\u25a2')
                elif mm2 == 0:
                    plist.append('\u25a9')
                elif mm2 == 'X':
                    plist.append('\u25c9')
                else:
                    plist.append('\u25A0')
            print(f"{'  '.join(plist)}" + '\n')

    print("Solved")


# Level 1 - Bloxorz game map - 1 - Walkable terrain, 0 - No terrain, 9 - Goal

game_map = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]

solve_map(game_map, (1, 1, 1, 1))
