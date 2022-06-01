from __future__ import annotations
 
from MatrixSparse import *
from Position import *
from typing import Dict
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
    MSG_setter = "__setitem__() invalid arguments"

    def __init__(self, zero: float = 0.0):
        if not isinstance(zero, (int, float)):
            raise ValueError("__init__() invalid arguments")
        #super() para chamar a classe correta, devido às inheritances
        super().__init__(zero)
        self._items = {}

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
        self.actual = 0
        self.max = len(self._items)
        self.iter_matrix = list(self._items)
        return self

    def __next__(self):
        if(self.actual < self.max):
            key = self.iter_matrix[self.actual]
            self.actual += 1
            return key
        else:
            raise StopIteration
    
    def __getitem__(self, pos: tuple[Position, position]) -> float:
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

    def __setitem__(self, pos: tuple[Position, position], val: tuple[int, float]):
        #if pos is a tuple(position) or a Position and val is and int or a float, 
        #and in the case pos is a tuple(position) with 2 values, and both values are int, and both values zero or
        #positive (no negative places on matrices), and val is different than self._zero (matrix zero), sets the value
        #otherwise if pos is a Position and val is different than self._zero (matrix zero), sets the value

        if isinstance(val,(float,int)) and isinstance(pos,(Position,tuple)):
            if isinstance(pos, Position):
                if val != self.zero:
                    self._items[pos] = val
                elif pos in self._items:
                    del self._items[pos]
            elif isinstance(pos, tuple) and len(pos) == 2 and isinstance(pos[0],int) and isinstance(pos[1],int) and pos[0] >= 0 and pos[1] >= 0:
                if val != self.zero:
                    self._items[Position(pos[0],pos[1])] = val
                elif Position(pos[0],pos[1]) in self._items:
                    del self._items[Position(pos[0],pos[1])]
            else:
                raise ValueError(self.MSG_setter)
        else:
            raise ValueError(self.MSG_setter)
 
    def __len__(self) -> int:
        return len(self._items)

#    def _add_number(self, other: [int, float]) -> Matrix:
    def _add_number(self, pos: tuple[Position,position] ,val: tuple[int, float]) -> Matrix:
        if isinstance(val,(float,int)) and isinstance(pos,(Position,tuple)) and isinstance(pos[0],int) and isinstance(pos[1],int) and pos[0] >= 0 and pos[1] >= 0:
                if val != self.zero:
                    self._items[pos] = val
                elif pos in self._items:
                    del self._items[pos]
                raise ValueError(self.MSG_setter)
        else:
            raise ValueError(self.MSG_setter)

    def _add_matrix(self, other: MatrixSparse) -> MatrixSparse:
        pass

#    def _mul_number(self, other: [int, float]) -> Matrix:
    def _mul_number(self, other) -> Matrix:
        pass

    def _mul_matrix(self, other: MatrixSparse) -> MatrixSparse:
        pass

    def dim(self) -> tuple[Position, position]:
        #apanha os valores (posições) minimos e maximos do teste, verifica se cada um é o maior ou o menor, e retorna-os

        if bool(self._items):
            position = list(self._items)
            row_min = position[0][0]
            col_min = position[0][1]
            row_max = position[0][0]
            col_max = position[0][1]
            for pos in position:
                if pos[0] > row_max:
                    row_max = pos[0]
                if pos[0] < row_min:
                    row_min = pos[0]
                if pos[1] > col_max:
                    col_max = pos[1]
                if pos[1] < col_min:
                    col_min = pos[1]
            return (Position(row_min, col_min), Position(row_max, col_max))
        return ()
        
    def row(self, row: int) -> Matrix:
        rowMatrix = MatrixSparseDOK(self.zero)
        if isinstance(row, int) and row >= 0:
            for key in self:
                if(key[0] == row):
                    rowMatrix[key] = self[key]
            return rowMatrix

    def col(self, col: int) -> Matrix:
        colMatrix = MatrixSparseDOK(self.zero)
        if isinstance(col, int) and col >= 0:
            for key in self:
                if(key[1] == col):
                    colMatrix[key] = self[key]
            return colMatrix

    def diagonal(self) -> Matrix:
        diagMatrix = MatrixSparseDOK(self.zero)
        for key in self:
            if(key[1] == key[0]):
                diagMatrix[key] = self[key]
        return diagMatrix

    @staticmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparseDOK:
        if isinstance(size,int) and size >=0  and isinstance(unitary,(int,float)) and isinstance(zero,(int,float)):
            spmax  = MatrixSparseDOK(zero)
            if size >= 0:
                for x in range(size):
                    for y in range(size):
                        if x == y:
                            spmax[(x,y)] = float(unitary)
                        else:
                            spmax[(x,y)] = zero
                return spmax
        else:
            raise ValueError("eye() invalid parameters")

    def transpose(self) -> MatrixSparseDOK:
        self.transposeMatrix = MatrixSparseDOK(self.zero)
        for key in self:
            self.transposeMatrix[key[1],key[0]] = self[key[0],key[1]]
        return self.transposeMatrix


    def compress(self) -> compressed:
        pass

    @staticmethod
    def doi(compressed_vector: compressed, pos: Position) -> float:
        pass

    @staticmethod
    def decompress(compressed_vector: compressed) -> MatrixSparse:
        pass
