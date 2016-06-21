import numpy as np
from scipy.sparse import spmatrix, coo_matrix


class Block(object):

    """docstring for ClassName"""
    
    def __init__(self, matrix):
        if matrix is not None:
            self.shape = matrix.shape
        else:
            self.shape = None

        if isinstance(matrix,np.ndarray):
            self.matrix = coo_matrix(matrix)
        else:
            self.matrix  = matrix

    def __str__(self):
        return self.matrix.__str__()

    def __repr__(self):
        return " Block : " + self.matrix.__repr__()

    def __add__(self, other):

        if isinstance(other,Block) is False:
            raise TypeError('Both Matrices should be of Block type')

        if self.matrix is not None and other.matrix is not None:
            return Block(self.matrix + other.matrix)
        elif self.matrix is None:
            return Block(other.matrix)
        else:
            return Block(self.matrix)

    def __mul__(self, other):
        
        if isinstance(other,Block) is False:
            raise TypeError('Both Matrices should be of Block type')

        if self.matrix is not None and other.matrix is not None:
            # print "self has shape", self.matrix.shape
            # print "other has shape", other.matrix.shape
            return Block(self.matrix.dot(other.matrix))
        else:
            return None

    def transpose(self):
        return Block(self.matrix.transpose())

    def dot(self, other):

        if isinstance(other,Block) is False:
            raise TypeError('Both Matrices should be of Block type')

        if self.matrix is not None and other.matrix is not None:
            return Block(self.matrix.dot(other.matrix))
        else:
            return None

    def __getattr__(self, attr):

        try:
            return getattr(self.matrix,attr)
        except AttributeError:
            raise AttributeError('Given Block does not have attribute', attr)




class BlockMatrix(np.ndarray):
    """docstring for BlockMatrix"""

    def __new__(cls,mblocks):
        # print type(mblocks)
        obj = np.asarray(mblocks)
        if obj.ndim !=2:
            raise ValueError('BlockMatrix must be 2-D. Kindly use BlockVector class for 1-D')
        return obj.view(cls)

    def __str__(self):
        return str(self.__array__())

    def __repr__(self):
        return repr(self.__array__()).replace('array','BlockMatrix')

    def __array_finalize__(self, obj):
        
        # print "Object is of type ", type(obj)
        # print "Self is of type", type(self)
        # print "Self has shape", self.shape

        for i in range(obj.shape[0]):
            for j in range(obj.shape[1]):
              if isinstance(obj[i,j],Block) is False and isinstance(obj[i,j], BlockMatrix) is False:
                  obj[i,j] = Block(obj[i,j])
        
        self.Row_Length = np.zeros(self.shape[0], dtype=np.int64)
        self.Col_Length = np.zeros(self.shape[1], dtype=np.int64)

        # print"Checking Validity"

        for i in range(obj.shape[0]):
            for j in range(obj.shape[1]):
                if obj[i,j].matrix is not None:
                    if self.Row_Length[i] == 0:
                        if isinstance(obj[i,j], Block):
                            if obj[i,j].matrix is not None:
                                self.Row_Length[i] = obj[i,j].shape[0]
                        elif isinstance(obj[i,j],BlockMatrix):
                            self.Row_Length[i] = sum(obj[i,j].Row_Length)
                        else:
                            raise ValueError('blocks must be either sparse matrix or BlockMatrix objects')
                    else:
                        if self.Row_Length[i] != obj[i,j].shape[0]:
                            raise ValueError('blocks[%d,:] has incompatible row dimensions' % i)
                        
                    if self.Col_Length[j] == 0:
                        if isinstance(obj[i,j], Block):
                            if obj[i,j].matrix is not None:
                                self.Col_Length[j] = obj[i,j].shape[1]
                        elif isinstance(obj[i,j],BlockMatrix):
                            self.Col_Length[i] = sum(obj[i,j].Col_Length)
                        else:
                            raise ValueError('blocks must be either sparse matrix or BlockMatrix objects')
                    else:
                        if self.Col_Length[j] != obj[i,j].shape[1]:
                            raise ValueError('blocks[:,%d] has incompatible column dimensions' % j)
        
        # ensure that at least one value in each row and col is not None
        if self.Row_Length.min() == 0:
            raise ValueError('blocks[%d,:] is all None' % self.Row_Length.argmin())
        
        if self.Col_Length.min() == 0:
            raise ValueError('blocks[:,%d] is all None' % self.Col_Length.argmin())

        # print "Validity Check complete"
        
        self.msize = (sum(self.Row_Length),sum(self.Col_Length))
        
        if obj is None:
            return None
