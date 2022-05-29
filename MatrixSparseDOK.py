from __future__ import annotations

from MatrixSparse import *
from Position import *
from typing import Dict
matrix = Dict[Position, float]


class MatrixSparseDOK(MatrixSparse):
    _items = matrix
    MSG_setter = "__setitem__() invalid arguments"

    def __init__(self, zero: float = 0.0):
        if not isinstance(zero, (float, int)):
            raise ValueError("__init__() invalid arguments")
        super().__init__(zero)
        self._items = {}

    def __copy__(self):
        spmax = MatrixSparseDOK(self.zero)
        for key in self:
            spmax[key] = self[key]
        return spmax

    def __eq__(self, other: MatrixSparseDOK):
        if isinstance(other,MatrixSparseDOK):
            return self._items == other._items

  
    def __iter__(self):
        self.current_index = 0
        self.max = len(self._items)
        self.iter_aux = sorted(list(self._items))
        return self


    # next iterator element
    def __next__(self):
        if(self.current_index < self.max):
            sel_key = self.iter_aux[self.current_index]
            self.current_index += 1
            return sel_key
        else:
            raise StopIteration

    #get items
    def __getitem__(self, pos: tuple[Position, position]) -> float:
        if isinstance(pos,Position) :
            return self._items[pos] if pos in self._items else self.zero
        
        if isinstance(pos[0],int) and isinstance(pos[1],int):
            if pos[0] >= 0 and pos[1] >= 0:
                return self._items[Position(pos[0],pos[1])] if Position(pos[0],pos[1]) in self._items else self.zero
        raise ValueError("__getitem__() invalid arguments")

    def __setitem__(self, pos: tuple[Position, position], val: tuple[int, float]):
       
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

    def _add_number(self,pos: tuple[Position,position] ,val: tuple[int, float]) -> Matrix:
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
    
    def _add_matrix_auxl(dim_x_length,dim_y_length,dim_x_height,dim_y_height,self,other,dim_x,dim_y) -> MatrixSparse:
        if((dim_x_length == dim_y_length) and (dim_x_height == dim_y_height) and self.zero == other.zero):
            spmax = MatrixSparseDOK(self.zero)
            for x in range(dim_x_height):
                for y in range(dim_x_length):                 
                    if (self[x + dim_x[0][0], y + dim_x[0][1]] == self.zero):
                        if (other[x + dim_y[0][0], y + dim_y[0][1]] != self.zero):
                            spmax[x + dim_x[0][0], y + dim_x[0][1]] = other[x + dim_y[0][0], y + dim_y[0][1]]
                    else:
                        spmax[x + dim_x[0][0], y + dim_x[0][1]] = self[x + dim_x[0][0], y + dim_x[0][1]]

                    if (other[x + dim_y[0][0], y + dim_y[0][1]] == other.zero):
                        if (self[x + dim_x[0][0], y + dim_x[0][1]] != self.zero):
                            spmax[x + dim_x[0][0], y + dim_x[0][1]] += self[x + dim_x[0][0], y + dim_x[0][1]]
                    elif spmax[x + dim_y[0][0], y + dim_y[0][1]] != other.zero:
                        spmax[x + dim_y[0][0], y + dim_y[0][1]] += other[x + dim_y[0][0], y + dim_y[0][1]]
                    else:
                        spmax[x + dim_y[0][0], y + dim_y[0][1]] = other[x + dim_y[0][0], y + dim_y[0][1]]
            return spmax
        else:
            raise ValueError("_add_matrix() incompatible matrices")

    def _add_matrix(self, other: MatrixSparse) -> MatrixSparse:
        dim_x= self.dim()
        dim_y = other.dim()
        dim_x_length = (dim_x[1][1] - dim_x[0][1]) + 1
        dim_x_height = (dim_x[1][0] - dim_x[0][0]) + 1
        dim_y_length = (dim_y[1][1] - dim_y[0][1]) + 1
        dim_y_height = (dim_y[1][0] - dim_y[0][0]) + 1
        _add_matrix_auxl(dim_x_length,dim_y_length,dim_x_height,dim_y_height,self,other,dim_x,dim_y)

    def _mul_number(self, other: tuple[int, float]) -> Matrix:
        if isinstance(other, (int, float)):
            spmax_copy = self.__copy__()
            for key in self:
                spmax_copy[key] *= other
            return spmax_copy

    def _mul_matrix(self, other: MatrixSparse) -> MatrixSparse:

        dim_x = self.dim()
        dim_y = other.dim()
        dim_x_length = (dim_x[1][1] - dim_x[0][1]) + 1
        dim_y_height = (dim_y[1][0] - dim_y[0][0]) + 1
        max_row_x,max_col_x = dim_x[1]
        max_row_y,max_col_y = dim_y[1]
        min_row_x,min_col_x= dim_x[0]
        min_row_y,min_col_y = dim_y[0]

        if((dim_x_length != dim_y_height) or (self.zero != other.zero)):
            result = MatrixSparseDOK(self.zero)
            for x in range(min_row_x, max_row_x + 1):
                for y in range(min_col_y, min_col_y + 1):
                    spmax = 0
                    for k in range(dim_x_length):
                        if self[(x,k+min_col_x)] != self.zero and other[(k+min_row_y,y)] != other.zero:
                            spmax += self[(x,k+min_col_x)]*other[(k+min_row_y,y)]
                        else:
                            continue
                    result[(x,y)] = spmax
        else:
              raise ValueError("_mul_matrix() incompatible matrices")
        return result

    def dim(self) -> tuple[Position, position]:
        if (self._items):
            pos = list(self._items)
            min_r = pos[0][0]
            min_c = pos[0][1]
            max_r = pos[0][0]
            max_c = pos[0][1]
            for p in pos:
                if p[0] > max_r:
                    max_r = p[0]
                if p[0] < min_r:
                    min_r = p[0]
                if p[1] > max_c:
                    max_c = p[1]
                if p[1] < min_c:
                    min_c = p[1]
            return (Position(min_r, min_c), Position(max_r, max_c))
        return ()
    

    def row(self, row: int) -> Matrix:
        spmax = MatrixSparseDOK(self.zero)
        if isinstance(row,int) and row >= 0:
            for key in self:
                if(key[0] == row):
                    spmax[key] = self[key]
            return spmax

    def col(self, col: int) -> Matrix:
        spmax = MatrixSparseDOK(self.zero)
        if isinstance(col,int) and col >= 0:
            for key in self:
                if(key[1] == col):
                    spmax[key] = self[key]
            return spmax

    def diagonal(self) -> Matrix:
        spmax = MatrixSparseDOK(self.zero)
        for key in self:
            if(key[1] == key[0]):
                spmax[key] = self[key]
        return spmax

    @staticmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparseDOK:
        if isinstance(size,int)  and isinstance(unitary,(int,float)) and isinstance(zero,(int,float)):
            spmax  = MatrixSparseDOK(zero)
            if size >= 0:
                for i in range(size):
                    spmax[Position(i,i)] = unitary
                return spmax
        else:
            raise ValueError("eye() invalid parameters")

    def transpose(self) -> MatrixSparseDOK:
        spmax = MatrixSparseDOK(self.zero)
        for key in self:
            spmax[(key[1],key[0])] = self[key]
      
        return spmax 


    def compress(self) -> compressed:
        if self.sparsity() >= 0.5:
            values = []
            indexes = []
            rows = [] 
            non_null_elem = []
            upper_left, bottom_right = self.dim()
            min_row,min_col = upper_left
            max_row,max_col = bottom_right
            total_elem_row = max_col-min_col + 1
            total_rows = max_row-min_row + 1
            offsets = [0]*total_rows
            rows = []
            aux = []
            for x in range(min_row,max_row+1):
                aux = []
                for y in range(min_col,max_col+1):
                    aux.append(self[Position(x,y)])
                rows.append(aux)
            for row_num,row in enumerate(rows):
                count = 0
                for elem in row:
                    if elem != self.zero:
                        count += 1
                non_null_elem.append((row,count,row_num+min_row))
            for row in rows:
                print(row)
            rows = list(map(lambda x:(x[0],x[2]),sorted(non_null_elem, key = lambda x: x[1],reverse = True)))
            for c,aux in enumerate(rows):
                row,row_num = aux
                offset_idx = 0
                value_idx = 0
                row_elem_idx = 0
                done = False
                if (values):
                    while row_elem_idx < total_elem_row: 
                        if value_idx + offset_idx < len(values): 
                            if (values[value_idx+offset_idx] == self.zero or row[row_elem_idx] == self.zero): 
                                value_idx += 1
                                row_elem_idx += 1
                            else:
                                value_idx = 0
                                row_elem_idx = 0
                                offset_idx += 1
                        else:
                            break
                    for i,elem in enumerate(row):
                        if i + offset_idx < len(values):
                            indexes[i+offset_idx] = row_num if elem != self.zero else indexes[i+offset_idx]
                            values[i+offset_idx] = elem if elem != self.zero else values[i+offset_idx]   
                        else:
                            indexes.append(row_num if elem != self.zero else -1)
                            values.append(elem)
                        offsets[row_num-min_row] = offset_idx                           
                else:
                    values = row
                    indexes = list(map(lambda x: row_num if x != self.zero else -1,row)) 
                    offsets[0] = offset_idx
            return ((min_row,min_col), self.zero, tuple(values), tuple(indexes), tuple(offsets))
        raise ValueError("compress() dense matrix")
    
    @staticmethod
    def doi(compressed_vector: compressed, pos: Position) -> float:
        if isinstance(compressed_vector,tuple) and isinstance(pos,Position):
            upper_left, zero, values, indices, offsets = compressed_vector
            if( isinstance(upper_left,tuple) and len(upper_left) == 2 and isinstance(zero,float) and isinstance(values,tuple) and isinstance(indices,tuple) and isinstance(offsets,tuple)):
                min_row, min_col = upper_left
                return values[pos[1] - min_col + offsets[pos[0]-min_row]] if indices[pos[1] - min_col + offsets[pos[0]-min_row]] == pos[0] else zero
        raise ValueError("doi() invalid parameters")
    @staticmethod
    def decompress(compressed_vector: compressed) -> MatrixSparse:
        if isinstance(compressed_vector,tuple):
            upper_left, zero, values, indices, offsets = compressed_vector
            if( isinstance(upper_left,tuple) and len(upper_left) == 2 and 
                isinstance(zero,float) and
                isinstance(values,tuple) and 
                isinstance(indices,tuple) and 
                isinstance(offsets,tuple)):

                min_row,min_col = upper_left
                spmax = MatrixSparseDOK(zero)
                x = 0
                for i,v in enumerate(values):
                    if(indices[i] != -1):
                        print("values: ",v)
                        print("indice",indices[i])
                        print("offset: ",offsets[indices[i] - min_row])
                        print()
                        spmax[Position(indices[i],i + min_col - offsets[indices[i] - min_row])] = v
                    else:
                        x += 1
                            
                return spmax
            raise ValueError("decompress() invalid parameters")

