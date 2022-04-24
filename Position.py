from __future__ import annotations


class Position:
    _pos = tuple[int, int]

    def __init__(self, row: int, col: int):
        if not (type(row) is int and row >= 0) or not (type(col) is int and col >= 0):
            raise ValueError('__init__() invalid arguments')
        self._pos = (row, col)

    def __str__(self):
        return "(" + str(self._pos[0]) + ", " + str(self._pos[1]) + ")"

    def __getitem__(self, item: int) -> int:
        if isinstance(item, int) and (item in (0, 1)):
            return self._pos[item]
        else:
            raise ValueError('__getitem__() invalid arguments')

    def __eq__(self, other: Position):
        return self._pos == other._pos

#CODIGO TIAGO
#creates a position in the dictionary Position_dict and increments its key count and returns the "position" value
def position_create(row: int, col: int):
    try:
        roww = int(row)
        colu = int(col)
    except:
        raise ValueError('position_create: invalid arguments')

    Position_dict [position] = roww, colu
    return position

#checks if the position exists in the dictionary, and returns true if it exists or false if the bool function returns "None", which means the position doesn't exist
def position_is(pos: position):
    return bool(Position_dict.get(position))

def position_row(pos: position):
    try:
        pos1 = position(pos)
    except:
        raise ValueError('position_row: invalid arguments')

    return position.row

def position_col(pos: position):
    try:
        pos1 = position(pos)
    except:
        raise ValueError('position_col: invalid arguments')

    return position.column

def position_equal(pos1: position, pos2: position):
    try:
        posi1 = position(pos1)
        posi2 = position(pos2)
    except:
        raise ValueError('position_equal: invalid arguments')

    return bool(pos1 = pos2)

str()