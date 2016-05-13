import numpy as np
from scipy.sparse import spmatrix
from scipy.sparse import coo_matrix

class BlockMatrix(object):

	def __init__(self, blocks):
		
		self.mblocks = np.asarray(blocks, dtype='object')
		if self.mblocks.ndim != 2:
				raise ValueError('blocks must be 2-D')		
		
		self.shape = self.mblocks.shape
		self.checkValidity()
		# self.skeleton = self.GetSkeleton()		
		# self.isCompatible(self.skeleton)
		# print type(self.mblocks)

	def getGlobalRowLength(self):
		RowLength = np.zeros(self.shape[0], dtype=np.int64)
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				if self.mblocks[i,j] is not None:
					# print "recognised ",(i,j), "As not null"
					if RowLength[i] ==0:
						if isinstance(self.mblocks[i,j], spmatrix):
							RowLength[i] = self.mblocks[i,j].shape[0]
						else:
							RowLength[i] = self.mblocks[i,j].getGlobalRowLength()

		return sum(RowLength) 					

	def getGlobalColLength(self):
		ColLength = np.zeros(self.shape[1], dtype=np.int64)
		for i in range(self.shape[0]):
			for j in range(self.shape[1]):
				if self.mblocks[i,j] is not None:

					if ColLength[i] ==0:
						if isinstance(self.mblocks[i,j], spmatrix):
							ColLength[i] = self.mblocks[i,j].shape[1]
						else:
							ColLength[i] = self.mblocks[i,j].getGlobalColLength()

		return sum(ColLength)

	def getSize(self):
		rows = self.getGlobalRowLength()
		cols = self.getGlobalColLength()
		return (rows,cols)	

	def checkValidity(self):

		block_mask = np.zeros(self.shape, dtype=bool)
		brow_lengths = np.zeros(self.shape[0], dtype=np.int64)
		bcol_lengths = np.zeros(self.shape[1], dtype=np.int64)

		
		for i in range(self.shape[0]):
		    for j in range(self.shape[1]):
		        if self.mblocks[i,j] is not None:
		            block_mask[i,j] = True

		            if brow_lengths[i] == 0:
		            	if isinstance(self.mblocks[i,j], spmatrix):
		            		brow_lengths[i] = self.mblocks[i,j].shape[0]
		            	elif isinstance(self.mblocks[i,j],BlockMatrix):
		            		brow_lengths[i] = self.mblocks[i,j].getGlobalRowLength()
		            		#print self.mblocks[i,j].getGlobalRowLength()
		            	else:
		            		raise ValueError('blocks must be either sparse matrix or BlockMatrix objects')
		            else:
		                if brow_lengths[i] != self.mblocks[i,j].shape[0]:
		                    raise ValueError('blocks[%d,:] has incompatible row dimensions' % i)


		            if bcol_lengths[j] == 0:
		            	if isinstance(self.mblocks[i,j], spmatrix):
		            		bcol_lengths[j] = self.mblocks[i,j].shape[1]
		            	elif isinstance(self.mblocks[i,j],BlockMatrix):
		            		bcol_lengths[i] = self.mblocks[i,j].getGlobalColLength()
		            		#print self.mblocks[i,j].getGlobalColLength()
		            	else:
		            		raise ValueError('blocks must be either sparse matrix or BlockMatrix objects')
		            else:
		                if bcol_lengths[j] != self.mblocks[i,j].shape[1]:
		                    raise ValueError('blocks[:,%d] has incompatible column dimensions' % j)
		                
		# print brow_lengths
		# print bcol_lengths

		# ensure that at least one value in each row and col is not None
		if brow_lengths.min() == 0:
		    raise ValueError('blocks[%d,:] is all None' % brow_lengths.argmin())
		if bcol_lengths.min() == 0:
		    raise ValueError('blocks[:,%d] is all None' % bcol_lengths.argmin())

		# print "The matrix is all set"

	def bmatvec(self,other):
		# other to be of type BlockVector
		pass


class BlockVector(object):
	

	# Do I need this?
	# def __new__(cls, *args, **kwargs):
	# 	pass

	def __init__(self, blocks):

		self.vblocks = np.asarray(blocks, dtype='object')
		if self.vblocks.ndim != 1:
				raise ValueError('blocks must be 1-D')

		self.shape = self.vblocks.shape[0]
		print self.shape

		#Take all to COO format
		for i in range(self.shape):
			if self.vblocks[i] is not None:
				self.vblocks[i] = coo_matrix(self.vblocks[i])

		# print type(self.vblocks)
		# print self

		#change all 1-D arrays in to compatible form, or demand user to tweak that?


	def checkValidty(self):
		#issue warning if any block is more than 1 D
		pass

	def isPreCompatible(self,other):
		#expecting the other to be of type BlockMatrix, Error check needed?
		if(self.shape==other.shape[1]):
			return True
		else:
			return False

	def isPostCompatible(self,other):
		#expecting the other to be of type BlockMatrix, Error check needed?
		if(self.shape==other.shape[0]):
			return True
		else:
			return False

	def __add__(self,other):

		if(self.shape == other.shape):
			S = np.asarray([None]*self.shape)

			for i in range(self.shape):
				print i
				if self.vblocks[i] is not None and other.vblocks[i] is not None:
					S[i] = self.vblocks[i] + other.vblocks[i]
					print "add"		
				elif self.vblocks[i] is None:
					print "self block is", self.vblocks[i]
					print "other block is ", other.vblocks[i]
					S[i] = other.vblocks[i]
					print "other"
				else: 
					S[i] = self.vblocks[i]
					print "self"
			return BlockVector(S)
		else:
			return NotImplemented 


##### The following is just test code, to be removed #####
from scipy.sparse import coo_matrix, csc_matrix, bmat
A = coo_matrix([[1, 2,7], [3, 4,8],[3,4,4]])
#A = np.matrix([[1, 2 ], [5, 6 ]])
B = coo_matrix([[5], [6],[9]])
C = csc_matrix([[7]])
BM = BlockMatrix([[A, B], [None, C]]
# print BM.getSize()
# print BM.mblocks
# print type(BM)
M = BlockMatrix([[BM, None],[None,BM]])
# print M
# print type(M)
J = BlockMatrix([[M, None],[None, M]])
# print type(J)
print J.getSize()
BV1 = BlockVector([B, None, None])
BV2 = BlockVector([None, B, None])
# BV3 = BlockVector([A])
# print BV3.vblocks

# for i in range(BV1.shape):
# 	print i
# 	if type(BV1.vblocks[i]) is None:
# 		print "BV1 is noted to be null"

# 	print "BV1",i,BV1.vblocks[i], BV1.vblocks[i].shape
# 	print "BV2",i,BV2.vblocks[i], BV2.vblocks[i].shape
print BV1.vblocks
print BV2.vblocks
V  = BV1 + BV2
print V.vblocks
# print V.vblocks