from __future__ import annotations

from typing import Tuple



class Position:
    _pos = Tuple[int, int]

    def __init__(self, row: int, col: int):
        if isinstance(row,(float,int)) and isinstance(col,(float,int)):
            if col >= 0 and row >= 0:
                self._pos = (row,col)
        else:
            raise ValueError

    def __str__(self):
        return str(self._pos)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self._pos)

    def __getitem__(self, item: int) -> int:
        # Nao sei o que acontece se se pedir um indice inválido
        if isinstance(item,int):
            return self._pos[item]

    def __eq__(self, other: Position):
        if isinstance(other,Position):
            return self._pos == other._pos
        return False
    
    def __lt__(self,other):
        if isinstance(other,Position):
            if self[0] < other[0]:
                return True
            elif self[0] == other[0]:
                if self[1] < other[1]:
                    return True
            return False
        
