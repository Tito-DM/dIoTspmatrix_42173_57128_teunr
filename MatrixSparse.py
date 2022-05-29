from __future__ import annotations
from Matrix import *

position = tuple[int, int]
compressed = tuple[position, float, tuple[float, ...], tuple[int], ..., tuple[int, ...]]



class MatrixSparse(Matrix):
    _zero = float

    def __init__(self, zero):
        if type(zero) is float:
            self._zero = zero
        else: raise ValueError("__init__() invalid arguments")

    @property
    def zero(self) -> float:
        return self._zero

    @zero.setter
    def zero(self, val: float):
        for key in self:
            if(self[key] == self._zero):
                del self._items[key]
        if type(val) is int:
            val_float = float (val)
            self._zero = val_float
        if type(val) is float:
            self._zero = val
            
        
    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    def sparsity(self) -> float: #o sparsity só adiciona 2 posições, a primeira e a ultima, daí só precisar comprarar ambas
        positions = self.dim()
        if bool(self._items):
            row_min, col_min = positions[0]
            row_max, col_max = positions[1]
            total_elem = (col_max - col_min + 1) * (row_max - row_min + 1)
            zero_null = total_elem - len(self._items)

            return zero_null/float(total_elem)
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
