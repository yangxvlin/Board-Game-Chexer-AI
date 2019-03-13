
# main function, similar to c or java, to do little test


from Board import Board

from Hexa import Hexa
import numpy as np

# a = [[Hexa(1,1), Hexa(2,2)], [Hexa(3,3), Hexa(4,4)]]
# b = [Hexa(5,5), Hexa(6,6)]
# a.append(b)
#
# c = np.array(a)
#
# [r, col] = c.shape
# for i in range(r):
#     for j in range(col):
#         c[i][j].print_hexa()

b = Board()
b.print_board()
