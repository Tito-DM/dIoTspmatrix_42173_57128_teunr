from __future__ import annotations
 
from MatrixSparse import *
from Position import *
from typing import Dict
spmatrix = Dict[Position, float]




class MatrixSparseDOK(MatrixSparse):
    _items = spmatrix
    MSG_setter = "__setitem__() invalid arguments"

    def __init__(self, zero: float = 0.0):
        # if the zero is not an int nor a float, initializes a matrix
        if not isinstance(zero, (int, float)):
            raise ValueError("__init__() invalid arguments")
        #super() para chamar a classe correta, devido às inheritances
        super().__init__(zero)
        self._items = {}

    def __copy__(self):
        #for each existing key in the self matrix, creates a similar one on the copy matrix
        copy = MatrixSparseDOK(self.zero)
        for key in self:
            copy[key] = self[key]
        return copy

    def __eq__(self, other: MatrixSparseDOK):
        #copies the other matrix items to the self matrix items
          if isinstance(other,MatrixSparseDOK):
            return self._items == other._items

    def __iter__(self):

        self.actual = 0
        self.max = len(self._items)
        self.iterMatrix = sorted(self._items,key=lambda x: x[self.actual]) #sort by row

        self.actual = 0 #new parameter indicating the key being worked on
        self.max = len(self._items) #new parameter indicating the number of keys
        self.iterMatrix = sorted(self._items,key=lambda x: x[0]) #new parameter with a list of the items sorted by row

        return self

    def __next__(self):
        if(self.actual < self.max): 
            key = self.iterMatrix[self.actual] #the key being worked is the actual, using the sorted matrix list
            self.actual += 1 #increments the key being worked on for later
            return key #returns the key to work on
        else:
            raise StopIteration #finishes the iterations
    
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
        return len(self._items) #returns the number of keys

    def _add_number(self, other: tuple[int, float]) -> Matrix:
        #creates a copy of the received matrix and adds "other" to its non-null values, then returns it
        if isinstance(other, (int, float)):
            newMatrix = self.__copy__()
            for key in self:
                newMatrix[key] += other
            return newMatrix

    def _add_matrix(self, other: MatrixSparse) -> MatrixSparse:
        dim1 = self.dim() 
        dim2 = other.dim()
        dim1_length = (dim1[1][1] - dim1[0][1]) + 1
        dim1_height = (dim1[1][0] - dim1[0][0]) + 1
        dim2_length = (dim2[1][1] - dim2[0][1]) + 1
        dim2_height = (dim2[1][0] - dim2[0][0]) + 1

        if((dim1_length == dim2_length) and (dim1_height == dim2_height) and self.zero == other.zero):
             
            spmatrix = MatrixSparseDOK(self.zero)
            for x in range(dim1_height):
                for y in range(dim1_length):                 
                    if (self[x + dim1[0][0], y + dim1[0][1]] == self.zero):
                        pass
                    else:
                        spmatrix[x + dim1[0][0], y + dim1[0][1]] = self[x + dim1[0][0], y + dim1[0][1]]

                    if (other[x + dim2[0][0], y + dim2[0][1]] == other.zero):
                        pass
                    elif  spmatrix[x + dim2[0][0], y + dim2[0][1]] != other.zero:
                         spmatrix[x + dim2[0][0], y + dim2[0][1]] += other[x + dim2[0][0], y + dim2[0][1]]
                    else:
                         spmatrix[x + dim2[0][0], y + dim2[0][1]] = other[x + dim2[0][0], y + dim2[0][1]]

            return  spmatrix
        else:
            raise ValueError("_add_matrix() incompatible matrices")

    def _mul_number(self, other: tuple[int,float]) -> Matrix:
        #creates a copy of the received matrix and multiplies "other" to its non-null values, then returns it
        if isinstance(other, (int, float)):
            newMatrix = self.__copy__()
            for key in self:
                newMatrix[key] *= other
            return newMatrix

    def _mul_matrix(self, other: MatrixSparse) -> MatrixSparse:
        dim1 = self.dim() 
        dim2 = other.dim() 
        dim1_length = (dim1[1][1] - dim1[0][1]) + 1 
        dim2_height = (dim2[1][0] - dim2[0][0]) + 1 
        
        max_row_1,max_col_1 = dim1[1]
        max_row_2,max_col_2 = dim2[1]

        min_row_1,min_col_1 = dim1[0]
        min_row_2,min_col_2 = dim2[0]

        if((dim1_length != dim2_height) or (self.zero != other.zero)):
            raise ValueError("_mul_matrix() incompatible matrices")
        else:
            result = MatrixSparseDOK(self.zero)
            for x in range(min_row_1, max_row_1 + 1):
                for y in range(min_col_2, max_col_2 + 1):
                    aux = 0
                    for k in range(dim1_length):
                        if self[(x,k+min_col_1)] != self.zero and other[(k+min_row_2,y)] != other.zero:
                            aux += self[(x,k+min_col_1)]*other[(k+min_row_2,y)]
                        else:
                            continue
                    result[(x,y)] = aux
        return result

    def dim(self) -> tuple[Position, position]:
        if (self._items):
            pos = list(self._items) #converts the dictionary to a list of tuples
            min_r = pos[0][0] #min row
            min_c = pos[0][1] #min column
            max_r = pos[0][0] #max row
            max_c = pos[0][1] #max column
            for p in pos:
                if p[0] > max_r: #if the row is greater than the current max row
                    max_r = p[0] #set the max row to the current row
                if p[0] < min_r: #if the row is smaller than the current min row
                    min_r = p[0] #set the min row to the current row
                if p[1] > max_c: #if the column is greater than the current max column
                    max_c = p[1] #set the max column to the current column
                if p[1] < min_c: #if the column is smaller than the current min column
                    min_c = p[1] #set the min column to the current column
            return (Position(min_r, min_c), Position(max_r, max_c)) #returns the minimum and maximum column and row values
        return () #returns empty
        
    def row(self, row: int) -> Matrix:
        #create an instance of MatrixSparseDOK 
        spmatrix_row = MatrixSparseDOK(self.zero)
        if isinstance(row, int) and row >= 0: #check if the received row is an integer and if it is positive
            for key in self:
                if(key[0] == row): #check if the received row is the same as the row of the key
                    spmatrix_row[key] = self[key] #if so, add the value of the key to the new matrix
            return spmatrix_row

    def col(self, col: int) -> Matrix:
        #create an instance of MatrixSparseDOK 
        spmatrix_col = MatrixSparseDOK(self.zero) #check if the received col is an integer and if it is positive
        if isinstance(col, int) and col >= 0:
            for key in self:
                if(key[1] == col): #check if the received row is the same as the col of the key
                    spmatrix_col[key] = self[key]  #if so, add the value of the key to the new matri
            return spmatrix_col

    def diagonal(self) -> Matrix:
        spmatrix_diagonal = MatrixSparseDOK(self.zero) #create an instance of MatrixSparseDOK
        for key in self:
            if(key[1] == key[0]): #check if the key is on the diagonal
                spmatrix_diagonal[key] = self[key] #if so, add the value of the key to the new matrix
        return spmatrix_diagonal

    @staticmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparseDOK:
        #check size,zeros and unitary values if are valid
        if isinstance(size,int) and size >=0  and isinstance(unitary,(int,float)) and isinstance(zero,(int,float)):
            #create a matrix with the received values
            spmax  = MatrixSparseDOK(zero)
            if size >= 0:
                for x in range(size):
                    for y in range(size):
                        if x == y: #if the position is on the diagonal example: (0,0)
                            spmax[(x,y)] = float(unitary) #set the the unitary value on the diagonal
                        else:
                            spmax[(x,y)] = zero #set the rest of the positions to zero
                return spmax
        else:
            raise ValueError("eye() invalid parameters")

    def transpose(self) -> MatrixSparseDOK:
        #create a new matrix with the transpose of the received matrix
        self.transposeMatrix = MatrixSparseDOK(self.zero)
        for key in self:
            self.transposeMatrix[key[1],key[0]] = self[key[0],key[1]] #set the transpose of the received matrix
        return self.transposeMatrix


    def compress(self) -> compressed:
        if self.sparsity() >= 0.5: 
            #set variables
            values_container = []
            indexes_container = []
            rows_container = [] 
            non_null_container = []
            upper_l, bottom_r = self.dim() #get the upper left and bottom right positions of the matrix
            min_row,min_col = upper_l
            max_row,max_col = bottom_r
            total_elem_row = max_col-min_col + 1
            total_rows = max_row-min_row + 1
            offsets = [0]*total_rows
            spmax = []


            for x in range(min_row,max_row+1):
                #populate the rows list with the number of elements in each row
                for y in range(min_col,max_col+1):
                    spmax.append(self[Position(x,y)])
                rows_container.append(spmax)
            #populate tge non_null_elem list with the non null elements of the matrix
            for row_num,row in enumerate(rows_container):
                count = 0
                for elem in row:
                    if elem != self.zero: #check if the element is not zero element
                        count += 1
                non_null_container.append((row,count,row_num+min_row)) #add the row, the number of non-null elements and the row number to the list
          
            rows_container = list(map(lambda x:(x[0],x[2]),sorted(non_null_container, key = lambda x: x[1],reverse = True))) #sort the rows by the number of non-null elements
            for c,spmax in enumerate(rows_container): 
                row,row_num = spmax
                offset_idx = 0
                value_idx = 0
                row_elem_idx = 0
                if (values_container):
                    while row_elem_idx < total_elem_row: #check if the row is not empty
                        if value_idx + offset_idx < len(values_container): #check if the value index is not out of range
                            if (values_container[value_idx+offset_idx] == self.zero or row[row_elem_idx] == self.zero): 
                                value_idx += 1
                                row_elem_idx += 1
                            else:
                                value_idx = 0
                                row_elem_idx = 0
                                offset_idx += 1
                        else:
                            break
                    for i,elem in enumerate(rows_container):
                        if i + offset_idx < len(values_container): #check if the value index is not out of range
                           indexes_container[i+offset_idx] = row_num  if elem != self.zero else indexes_container[i+offset_idx] #if the element is not zero, set the row number
                           values_container[i+offset_idx] = elem if elem != self.zero else values_container[i+offset_idx]   #if the element is not zero, set the value
                        else:
                            indexes_container.append(row_num if elem != self.zero else -1)
                            values_container.append(elem)
                        offsets[row_num-min_row] = offset_idx                           
                else:
                    values_container = rows_container
                    indexes_container = list(map(lambda x: row_num if x != self.zero else -1,row)) 
                    offsets[0] = offset_idx
            return ((min_row,min_col), self.zero, tuple(values_container), tuple(indexes_container), tuple(offsets))
        raise ValueError("compress() dense matrix")
    

    @staticmethod
    def doi(compressed_vector: compressed, pos: Position) -> float:
        #check if compressed_vector is a compressed vector and pos is a Position
        if isinstance(compressed_vector,tuple) and isinstance(pos,Position):
            up_left, zero, val, index, offsets = compressed_vector #get the values of the compressed vector
            if( isinstance(up_left,tuple) and
             len(up_left) == 2 and isinstance(zero,float) and
              isinstance(val,tuple) and isinstance(index,tuple) and 
              isinstance(offsets,tuple)):
                min_row, min_col = up_left #get the upper left position of the compressed vector
                if index[pos[1] - min_col + offsets[pos[0]-min_row]] == pos[0]: #check if the position is in the compressed vector
                    return val[pos[1] - min_col + offsets[pos[0]-min_row]] #return the value of the position
                else:
                    return zero
        raise ValueError("doi() invalid parameters")

    @staticmethod
    def decompress(compressed_vector: compressed) -> MatrixSparse:
        #check if compressed_vector is a compressed vector
        if isinstance(compressed_vector,tuple):
            up_left, zero, values, index, offsets = compressed_vector #get the values of the compressed vector
            if( isinstance(up_left,tuple) and 
                isinstance(zero,float) and
                isinstance(values,tuple) and 
                isinstance(index,tuple) and 
                isinstance(offsets,tuple)):

                min_row,min_col = up_left #get the upper left position of the compressed vector
                spmax = MatrixSparseDOK(zero) #create a new matrix with the same zero value
                x = 0
                for i,v in enumerate(values):
                    if(index[i] != -1):
                        spmax[Position(index[i],i + min_col - offsets[index[i] - min_row])] = v #set the value of the position
                    else:
                        x += 1 #count the number of zero elements
                return spmax
            raise ValueError("decompress() invalid parameters")
