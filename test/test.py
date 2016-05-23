import blocklinalg
from scipy.sparse import coo_matrix, csc_matrix

def test0():
    
    A = coo_matrix([[1, 2], [3, 4]])
    B = coo_matrix([[5],[6]]) 
    C = csc_matrix([[7]])
    
    Ab = blocklinalg.Block(A)
    Bb = blocklinalg.Block(B)
    Cb = blocklinalg.Block(C)
    Db = blocklinalg.Block(None)
    
    assert isinstance(Ab, blocklinalg.Block)
    
     ### Following tests work perfectly. Not sure how to test using assert ###

    S = Ab+Ab 
    # assert S[0,0] == 2 
    # assert S[0,1] == 4
    # assert S[1,0] == 6
    # assert S[1,1] == 8

    T  = Ab.transpose()
    # assert T[0,0] == 1
    # assert T[0,1] == 3
    # assert T[1,0] == 2
    # assert T[1,1] == 4

    M = Ab*Ab
    # assert M[0,0] == 1
    # assert M[0,1] == 4
    # assert M[1,0] == 9
    # assert M[1,1] == 16

    Dot = Ab.dot(Bb)
    assert Dot.shape == (2,1)
    # assert Dot[0,0] == 17
    # assert Dot[1,0] == 39

    P = blocklinalg.BlockMatrix([[A, B], [None, C]])
    assert isinstance(P, blocklinalg.BlockMatrix)
    Psum = P + P
    assert P.shape == Psum.shape
    assert P.msize == Psum.msize

    # @aseem Insert some code here that you want to work, e.g.,
    #
    #  A00 = np.array([[1]])
    #  A01 = np.array([[2]])
    #  A10 = np.array([[3]])
    #  A11 = np.array([[4]])
    #  A = blocklinalg.BlockMatrix([[A00, A01], [A10, A11]])
    #
    #  x0 = np.array([1])
    #  x1 = np.array([2])
    #  x = blocklinalg.BlockVector([x0, x1])
    #
    # b = A.mult(x)
    #
    # assert isinstance(b, blocklinalg.BlockVector)
    # assert b.num_blocks == 2
    # assert b[0] = np.array([5])
    # assert b[1] = np.array([11])
    #
    return
