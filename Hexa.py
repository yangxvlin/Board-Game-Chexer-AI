# each hexa contains some coordinates
# x, y, z for cube coordinates
# two of x, y, z for axial coordinate

# using axial coordiante for storing
class Hexa:

    def __init__(self, q, r):
        self.q = q
        self.r = r

    def print_hexa(self):
        print("(" + str(self.q) + ", " + str(self.r) + ")", end="")