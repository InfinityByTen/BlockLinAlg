# BlockLinAlg
BlockLinAlg is planned to be a Scipy and Numpy based module for Linear Algebra Routines with blocked structure

This is the setup for a Block Class that encapsulates different matrices. numpy dense and scipy sparse are direct targets for now. Eventually the possibility of type agnostic matrices can be considered. 

The BlockMatrix and the upcoming BlockVector classes are planned to be derived classes of scipy.ndarray to make the background work smoothly. A way to restrict / cast the ndarray elements to Block objects is sought.

This piece of software is still under active development (as on May 2016); comments, suggestions and improvements are always welcome. At the juncture, this is an incomplete, yet functional outline for the intended module. Kindly direct your correspondence to  dua<at>math<dot>tu<hyphen>berlin<dot>de.

Cheers!
Aseem Dua
