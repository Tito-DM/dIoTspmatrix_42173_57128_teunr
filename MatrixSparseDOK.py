from __future__ import annotations
from ast import List
from typing import Dict
from MatrixSparse import *
from Position import *

spmatrix = Dict[Position, float]

# zero=0.0
# (1,2), 4.5
# (1,3), 1.1
# (1,4), 4.5
# (1,5), 2.1
# (1,6), 3.3
# (2,2), 4.5
# (2,3), 4.5


class MatrixSparseDOK(MatrixSparse):
    _items = spmatrix

    def __init__(self, zero: float = 0.0):
        if not isinstance(zero, (int, float)):
            raise ValueError("__init__() invalid arguments")
        self._items = {(0, 0): zero}


    def __copy__(self):
        copy = MatrixSparseDOK(self.zero)
        for key in self:
            copy[key] = self[key]
            
        return copy

    def __eq__(self, other: MatrixSparseDOK):
        if(self._items == other._items):
            return True
        return False

    def __iter__(self):
        pass

    def __next__(self):
        pass
    
    def __getitem__(self, pos: [Position, position]) -> float:
        #if pos is a tuple(position) with 2 values, and both values are int, and both values zero or 
        # positive (no negative places on matrices), if that position exists, returns it, otherwise returns zero
        if type (pos) is tuple and len(pos) == 2: 
            if type(pos[0]) is int and type(pos[1]) is int and pos[0] >= 0 and pos[1] >= 0:
                if Position(pos[0], pos[1]) in self._items: 
                    return self._items[Position(pos[0], pos[1])] 
                else:
                    return self.zero 
        #it pos is a Position, and that position exists, returns it, otherwise returns zero
        if type (pos) is Position: 
            if pos in self._items: 
                return self._items[pos] 
            else:
                return self.zero 
        #if none of the previous are met, raises ValueError
        raise ValueError("__getitem__() invalid arguments")

    def __setitem__(self, pos: [Position, position], val: [int, float]):
        #if pos is a tuple(position) or a Position and val is and int or a float, 
        #and in the case pos is a tuple(position) with 2 values, and both values are int, and both values zero or
        #positive (no negative places on matrices), and val is different than self.zero (matrix zero), sets the value
        #otherwise if pos is a Position and val is different than self.zero (matrix zero), sets the value

        if isinstance(pos, (tuple,Position)) and isinstance(val, (int, float)):
            if type(pos) is tuple and len(pos) == 2:
                if type(pos[0]) is int and type(pos[1]) is int and pos[0] >= 0 and pos[1] >= 0:
                    if Position(pos[0], pos[1]) in self._items:
                        del self._items[Position(pos[0], pos[1])]
                    elif val != self.zero: 
                        self._items[Position(pos[0], pos[1])] = val
                    else: raise ValueError("__setitem__() invalid arguments")
                else: raise ValueError("__setitem__() invalid arguments")
            elif type (pos) is Position:
                if pos in self._items:
                    del self._items[pos]
                elif val != self.zero:
                    self._items[pos] = val
                else: raise ValueError("__setitem__() invalid arguments")
            else: raise ValueError("__setitem__() invalid arguments")
        else: raise ValueError("__setitem__() invalid arguments")
        # if isinstance(val,(float,int)) and isinstance(pos,(Position,tuple)):
        #     if isinstance(pos, Position):
        #         if val != self.zero:
        #             self._items[pos] = val
        #         elif pos in self._items:
        #             del self._items[pos]
        #     elif isinstance(pos, tuple) and len(pos) == 2 and isinstance(pos[0],int) and isinstance(pos[1],int) and pos[0] >= 0 and pos[1] >= 0:
        #         if val != self.zero:
        #             self._items[Position(pos[0],pos[1])] = val
        #         elif Position(pos[0],pos[1]) in self._items:
        #             del self._items[Position(pos[0],pos[1])]
        #     else:
        #         raise ValueError("__setitem__() invalid arguments")
        # else:
        #     raise ValueError("__setitem__() invalid arguments")
 
    def __len__(self) -> int:
        return len(self._items)

#    def _add_number(self, other: [int, float]) -> Matrix:
    def _add_number(self, other) -> Matrix:
        pass

    def _add_matrix(self, other: MatrixSparse) -> MatrixSparse:
        pass

#    def _mul_number(self, other: [int, float]) -> Matrix:
    def _mul_number(self, other) -> Matrix:
        pass

    def _mul_matrix(self, other: MatrixSparse) -> MatrixSparse:
        pass

    def dim(self) -> tuple[Position, position]:
        pass
        
    def row(self, row: int) -> Matrix:
        pass

    def col(self, col: int) -> Matrix:
       pass

    def diagonal(self) -> Matrix:
        pass

    @staticmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparseDOK:
        pass

    def transpose(self) -> MatrixSparseDOK:
        pass

    def compress(self) -> compressed:
        pass

    @staticmethod
    def doi(compressed_vector: compressed, pos: Position) -> float:
        pass

    @staticmethod
    def decompress(compressed_vector: compressed) -> MatrixSparse:
        pass
