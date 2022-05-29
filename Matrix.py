from __future__ import annotations
from abc import ABC, abstractmethod
from Position import *

class Matrix(ABC):

    @abstractmethod
    def __getitem__(self, item):
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, key, value):
        raise NotImplementedError

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @abstractmethod
    def __next__(self):
        raise NotImplementedError

    @abstractmethod
    def __copy__(self):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self._add_number(other)
        if isinstance(other, Matrix):
            return self._add_matrix(other)
        raise ValueError('_add__ invalid argument')

    @abstractmethod
    def _add_number(self, other: [int, float]) -> Matrix:
        raise NotImplementedError

    @abstractmethod
    def _add_matrix(self, val: Matrix) -> Matrix:
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self._mul_number(other)
        if isinstance(other, Matrix):
            return self._mul_matrix(other)
        raise ValueError('__mul__ invalid argument')

    @abstractmethod
    def _mul_number(self, other: [int, float]) -> Matrix:
        raise NotImplementedError

    @abstractmethod
    def _mul_matrix(self, other: Matrix) -> Matrix:
        raise NotImplementedError

    def __str__(self):
        string = ""
        d = self.dim()
        if len(d) == 2:
            up_left, down_right = d
            row_min,col_min = up_left
            row_max,col_max = down_right
            for x in range(row_min,row_max+1):
                for y in range(col_min,col_max+1):
                    #Caso o numero que for retornado seja um inteiro apresentalo como inteiro
                    if float(self[Position(x,y)]).is_integer():
                        string += str(int(self[Position(x,y)]))
                    else:
                        string += str(self[Position(x,y)])
                    #Nao colocar espaço no ultimo elemento de cada linha
                    if y != col_max:
                        string += " "
                #Não colocar \n no ultimo elemente da ultima linha
                if x != row_max:
                    string += "\n"
        return string

    @abstractmethod
    def dim(self) -> tuple[Position, ...]:
        raise NotImplementedError

    @abstractmethod
    def row(self, row: int) -> Matrix:
        raise NotImplementedError

    @abstractmethod
    def col(self, col: int) -> Matrix:
        raise NotImplementedError

    @abstractmethod
    def diagonal(self) -> Matrix:
        raise NotImplementedError

    @abstractmethod
    def transpose(self) -> Matrix:
        raise NotImplementedError
