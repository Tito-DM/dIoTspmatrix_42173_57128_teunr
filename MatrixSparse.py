from __future__ import annotations
from Matrix import *
from typing import Tuple


position = Tuple[int, int]
compressed = Tuple[position, float, Tuple[float], Tuple[int], Tuple[int]]

class MatrixSparse(Matrix):
    _zero = float

    def __init__(self, zero):
        self._zero = zero

    @property
    def zero(self) -> float:
        return self._zero

    #TODO: Ver como funciona
    @zero.setter
    def zero(self, val: float):
        if isinstance(val,(int,float)):
            self._zero = float(val)
        for key in self:
            if(self[key] == self._zero):
                del self._items[key]

                

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    def sparsity(self) -> float:
        pos = self.dim()
        if (self._items):
            min_r,min_c = pos[0]
            max_r,max_c = pos[1]
            total = (max_c-min_c+1)*(max_r-min_r+1)
            zero = total - len(self._items)
            return zero/float(total)
        else:
            return 1.0

    @staticmethod
    @abstractmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparse:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def compress(self) -> compressed:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def doi(compressed_vector: compressed, pos: Position) -> float:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decompress(compressed_vector: compressed) -> Matrix:
        raise NotImplementedError
