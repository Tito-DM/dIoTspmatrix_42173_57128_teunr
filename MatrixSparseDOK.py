from __future__ import annotations
from ast import List
from typing import Dict
from MatrixSparse import *
from Position import *

spmatrix = Dict[Position, float]


class MatrixSparseDOK(MatrixSparse):
    _items = spmatrix

    def __init__(self, zero: float = 0.0):
        if  (type(zero) is not float):
            raise ValueError("__init__() invalid arguments")
        self._items = {(0, 0): zero}

    def __copy__(self):
        if(type(self._items[0]) is not float):
            return self._items.copy()

    def __eq__(self, other: MatrixSparseDOK):
        if(self._items == other._items):
            return True
        return False

    def __iter__(self):
        pass

    def __next__(self):
        pass

#    def __getitem__(self, pos: [Position, position]) -> float:
    def __getitem__(self, pos) -> float:
        if not (type (pos) is list) or not (type (Position) is int) or not (type (position) is int) or not (Position >= 0) or not (position >= 0):
            raise ValueError("__getitem__() invalid arguments")
        #self._items[pos]
        return self._items.get(pos)

        
#    def __setitem__(self, pos: [Position, position], val: [int, float]):
#        if not (type (pos) is list) or not (Position >= 0) or not (position >= 0) or not (type (val) is int or type (val) is float) or not (val > 0):

    def __setitem__(self, pos, val):
        if not (type (pos) is tuple) or not (Position is int) or not (position is int) or not (Position >= 0) or not (position >= 0) or not (type (val) is float) or not (val > 0.0):
            raise ValueError("__setitem__() invalid arguments")
        self._items[pos] = val

    def __len__(self) -> int:
        pass

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

    def dim(self) -> tuple[Position, ...]:
        self.dim
        


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
