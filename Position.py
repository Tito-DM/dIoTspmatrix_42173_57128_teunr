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
from dataclasses import dataclass

#class/struct created
#example access: p = position(3, 7)

@dataclass
class position:
    row: int
    column: int


#creating DoK position
#empty dictionary
Position_dict ={} 
#creates a Position in the dictionary Position_dict and increments its key count and returns the "Position" value
def Position_create(row: int, col: int):
    try:
        roww = int(row)
        colu = int(col)
    except:
        raise ValueError('Position_create: invalid arguments')

    Position_dict [Position] = roww, colu
    return Position

#checks if the Position exists in the dictionary, and returns true if it exists or false if the bool function returns "None", which means the Position doesn't exist
def Position_is(pos: Position):
    return bool(Position_dict.get(Position))

def Position_row(pos: Position):
    try:
        pos1 = Position(pos)
    except:
        raise ValueError('Position_row: invalid arguments')

    return Position.row

def Position_col(pos: Position):
    try:
        pos1 = Position(pos)
    except:
        raise ValueError('Position_col: invalid arguments')

    return Position.column

def Position_equal(pos1: Position, pos2: Position):
    try:
        posi1 = Position(pos1)
        posi2 = Position(pos2)
    except:
        raise ValueError('Position_equal: invalid arguments')

    return bool(pos1 = pos2)

str()