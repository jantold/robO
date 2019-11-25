# Simple matrix (as array) operations and linear algebra
# Arrays sind gegenueber Python lists effizienter und einfacher zu handhaben.
#
# http://www.numpy.org/
# https://scipy.github.io/old-wiki/pages/Tentative_NumPy_Tutorial
#
# O. Bittel; 28.09.2017; Python 3.5

import numpy as np
import numpy.linalg as la

print("\nMatrix and vector operations:")
a = np.array( [[1,1],[0,1]] )
b = np.array( [[2,0],[3,4]] )
x = np.array([3,1])
y = np.array([1,2])
print('x =', x)
print('y =', y)
print('a =')
print(a)
print('b =')
print(b)

print('a.*b =')
print(a*b) # element wise multiplication

print('a*b =')
print(np.dot(a,b)) # matrix multiplication
print(a.dot(b)) # matrix multiplication

print('x*y =')
print(np.dot(x,y)) # scalar product
print(x.dot(y)) # scalar product

print("a*x =") # matrix vector product
print(np.dot(a,x))

x1 = [3,1] # vector as list
print("a*x1 =") # matrix vector product
print(np.dot(a,x1))

c = a+b # matrix sum
print(c)

print(c.T) # matrix transpose

# Matrix inverse
print("\nMatrix Inverse:")
d = la.inv(c)
print(d)
print(np.dot(c,d))
print(np.dot(d,c))

# Eigenvalue:
print("\nEigenvalue:")

sigma = np.array(
    [[12.25,        15*3**0.5/4],
     [15*3**0.5/4,  4.75 ]])
print(sigma)
v,d = la.eig(la.inv(sigma))
print(v)
print(d)

# Zero matrix:
print("\nZero matrix:")
z = np.zeros( (3,4) )
print(z)

# Identity matrix:
print("\nIdentity matrix:")
z = np.identity(3)
print(z)

# random matrix:
print("\nRandom matrix:")
print(np.random.random((2,10))) # argument is tupe (2,10)


# Slicing arrays:
print("\nSlicing arrays:")
z = np.array([
    [1,2,3,4],
    [5,6,7,8],
    [9,1,2,3]])
print(z[0:2,0:3])


# Stacking arrays together:
print("\nStacking arrays together:")
u = np.array([1, 2, 3, 4])
v = np.array([5, 6, 7, 8])
w = np.vstack((u,v)) # tuple (u,v) ist needed
print("w =")
print(w)
t = np.hstack((u,v)) # tuple (u,v) ist needed
print("t =")
print(t)

