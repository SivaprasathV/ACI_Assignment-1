# Importing libraries
from pprint import pprint
from math import sqrt, pow
import time
import sys, os
# import collections


def clear():
    os.system('cls')
# Intialising the map


class initPositionError(Exception):

    def __init__(self, message='Initial Position provided is not valid'):
        self.message = message
        super().__init__(self.message)


class blocks:

    def __init__(self, _map, pos):
        self.width = 2
        self.height = 1
        self.length = 2
        self.map = _map
        self.position = pos
        self.state = None
        self.move()

    def get_block_state(self):
        return self.state, self.position
        # x_pos = []
        # x_row = []
        # for _i in range(self.map.__len__()):
        #     for _j in range(self.map[_i].__len__()):
        #         if self.map[_i][_j] == 'X':
        #             x_row.append(_i+1)
        #             x_pos.append((_i+1, _j+1))
        #
        # if set(x_pos).__len__() == 1:
        #     return "Standing", x_pos
        # elif set(x_pos).__len__() == 2 and set(x_row).__len__() > 1:
        #     return "Lying Vertical", x_pos
        # elif set(x_pos).__len__() == 2:
        #     return "Lying Horizontal", x_pos
        # else:
        #     return "Block not in Map", self.position

    def possible_moves(self, cur_pos):
        possible_moves_list = []
        Ax_ = cur_pos[0][0]
        Ay_ = cur_pos[0][1]
        Bx_ = cur_pos[1][0]
        By_ = cur_pos[0][1]
        if self.state == ".":
            possible_moves_list.append([(Ax_, Ay_ + 1), (Ax_, Ay_ + 2)])
            possible_moves_list.append([(Ax_ - 1, Ay_), (Ax_ - 2, Ay_)])
            possible_moves_list.append([(Ax_ + 1, Ay_), (Ax_ + 2, Ay_)])
            possible_moves_list.append([(Ax_, Ay_ - 1), (Ax_, Ay_ - 2)])

        elif self.state == "|":
            possible_moves_list.append([(Ax_ - 1, Ay_), (Bx_ - 2, By_)])
            possible_moves_list.append([(Ax_ + 2, Ay_), (Bx_ + 1, By_)])
            possible_moves_list.append([(Ax_, Ay_ - 1), (Bx_, By_ - 1)])
            possible_moves_list.append([(Ax_, Ay_ + 1), (Bx_, By_ + 1)])

        else:
            possible_moves_list.append([(Ax_ - 1, Ay_), (Bx_ - 1, By_)])
            possible_moves_list.append([(Ax_ + 1, Ay_), (Bx_ + 1, By_)])
            possible_moves_list.append([(Ax_, Ay_ - 1), (Bx_, By_ - 2)])
            possible_moves_list.append([(Ax_, Ay_ + 2), (Bx_, By_ + 1)])

        move_list = []
        for pm in possible_moves_list:
            for pm_i in pm:
                if (pm_i[0] > 6 or pm_i[0] < 1 or pm_i[1] > 10 or pm_i[1] < 1):
                    possible_moves_list.pop(possible_moves_list.index(pm))
                    break

        for pm in possible_moves_list:
            if self.map[pm[0][0] - 1][pm[0][1] - 1] == 1 and self.map[pm[1][0] - 1][pm[1][1] - 1] == 1:
                move_list.append(pm)
            elif self.map[pm[0][0] - 1][pm[0][1] - 1] == 9 and self.map[pm[1][0] - 1][pm[1][1] - 1] == 9:
                move_list.append(pm)

        return move_list

    def check_pos(self, _pos_):
        block_state = self.get_block_state()
        posA = self.map[block_state[1][0][0] - 1][block_state[1][0][1] - 1]
        posB = self.map[block_state[1][0][0] - 1][block_state[1][0][1] - 1]
        if block_state[0] is None:
            if (posA == 1 and posB == 1) or (posA == 9 and posB == 9):
                return True
            else:
                raise initPositionError
        else:
            mv_list = self.possible_moves(self.position)
            if _pos_ in mv_list:
                return True
            else:
                return False

    def move(self, _pos_=None):
        if _pos_ is None:
            _pos_ = self.position
        if self.check_pos(_pos_):
            cur_pos = self.position
            _Ax = cur_pos[0][0]
            _Ay = cur_pos[0][1]
            _Bx = cur_pos[1][0]
            _By = cur_pos[1][1]
            self.map[_Ax - 1][_Ay - 1] = 1
            self.map[_Bx - 1][_By - 1] = 1
            Ax_ = _pos_[0][0]
            Ay_ = _pos_[0][1]
            Bx_ = _pos_[1][0]
            By_ = _pos_[1][1]
            self.map[Ax_ - 1][Ay_ - 1] = "X"
            self.map[Bx_ - 1][By_ - 1] = "X"
            self.position = _pos_
            if _pos_[0] == _pos_[1]:
                self.state = "."
            elif _pos_[0][1] == _pos_[1][1]:
                self.state = "|"
            else:
                self.state = "-"

    def check_goal_reach(self):
        goal_flag = 0
        for i_ in range(self.map.__len__()):
            for j_ in range(self.map[i_].__len__()):
                if self.map[i_][j_] == 9:
                    goal_flag = goal_flag + 1

        if goal_flag == 0:
            return True
        else:
            return False


def init_map():
    game_map = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 1, 1, 9, 1, 1],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 0]]
    return game_map


gmap = init_map()

pprint(gmap)

b = blocks(gmap, [(2, 2), (2, 2)])

while not (b.check_goal_reach()):
    m_list = b.possible_moves(b.position)
    goal_blk = tuple()
    for m in b.map:
        if 9 in m:
            goal_blk = (b.map.index(m) + 1, m.index(9) + 1)
            break
    # add weights to reach goal
    cur_pos = b.position
    Ax_ = cur_pos[0][0]
    Ay_ = cur_pos[0][1]
    Bx_ = cur_pos[1][0]
    By_ = cur_pos[1][1]
    Gx_ = goal_blk[0]
    Gy_ = goal_blk[1]
    A_dist = sqrt(pow(Ax_ - Gx_,2) + pow(Ay_ - Gy_,2))
    B_dist = sqrt(pow(Bx_ - Gx_,2) + pow(By_ - Gy_,2))

    weights_pm = {}
    for pm in m_list:
        _Ax = pm[0][0]
        _Ay = pm[0][1]
        _Bx = pm[1][0]
        _By = pm[1][1]
        _A_dist = sqrt(pow(_Ax - Gx_,2) + pow(_Ay - Gy_,2))
        _B_dist = sqrt(pow(_Bx - Gx_,2) + pow(_By - Gy_,2))

        weight = ((A_dist - _A_dist) + (B_dist - _B_dist)) / 2

        if weight in weights_pm.keys():
            weights_pm[weight].append(pm)
        else:
            weights_pm[weight] = [pm]

    ordered_weights_pm = {}

    for k in sorted(weights_pm.keys(),reverse=True):
        ordered_weights_pm[k] = weights_pm[k]

    for item in ordered_weights_pm:
        it_1 = ordered_weights_pm[item]
        if isinstance(it_1[0], list):
            clear()
            b.move(it_1[0])
        else:
            clear()
            b.move(it_1)
        pprint(b.map)
        time.sleep(2)
        break