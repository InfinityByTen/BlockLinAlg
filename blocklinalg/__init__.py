import numpy as np
from scipy.sparse import spmatrix

class Block(object):

	"""docstring for ClassName"""
	
	def __init__(self, matrix):
		if matrix is not None:
			self.shape = matrix.shape
		else:
			self.shape = None
		self.matrix  = matrix

	def __str__(self):
		return self.matrix.__str__()

	def __repr__(self):
		return self.matrix.__repr__()

	def __add__(self, other):

		if self.matrix is not None and other.matrix is not None:
			return Block(self.matrix + other.matrix)
		elif self.matrix is None:
			return Block(other.matrix)
		else:
			return Block(self.matrix)

	def __mul__(self, other):
		
		if self.matrix is not None and other.matrix is not None:
			if self.matrix.shape[1]==other.matrix.shape[0]:
				return Block(self.matrix.dot(other.matrix))
			else:
				raise ValueError('dimension mismatch')
		else:
			return None

	def dot(self, other):

		if self.matrix is not None and other.matrix is not None:
			return Block(self.matrix.dot(other.matrix))
		else:
			return None

class BlockMatrix(np.ndarray):
	"""docstring for BlockMatrix"""
	def __new__(cls,mblocks):
		print "I am inside BlockMatrix with class",cls,"and arguments",mblocks
		obj = np.asarray(mblocks).view(cls)
		return obj

	def __array_finalize__(self, obj):
		
		print "Object is of type ", type(obj)
		print "Self is of type", type(self)

		# self.shape = obj.shape
		
		# Check Validity 



		if obj is None:
			return None





		