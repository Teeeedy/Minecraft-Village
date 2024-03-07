from abstract_region import AbstractRegion
import sys

class RegionMap:
    region_arr = {}
    
    xMax = -sys.maxsize
    xMin = sys.maxsize
    zMax = -sys.maxsize
    zMin = sys.maxsize


    def __init__(self):
        self.region_arr = {}

    def get_val(self, x : int, z : int):
        return self.region_arr.get(x, {}).get(z, None)

    def set(self, x : int, z : int, val):
        self.xMin = min(x, self.xMin)
        self.xMax = max(x, self.xMax)
        self.zMin = min(z, self.zMin)
        self.zMax = max(z, self.zMax)

        if(self.region_arr.get(x) == None):
            self.region_arr[x] = {}

        self.region_arr[x][z] = val

    def display(self):
        for x in range(self.xMin, self.xMax + 1):
            for z in range(self.zMin, self.zMax + 1):
                reg = self.region_arr.get(x, {}).get(z, None)
                print("0" if reg == None else self.get_val(x, z), end=" ")
            print()
    
    def populateEmpty(self, size : int, val):
        #self.set(int(abs(size/2)), int(abs(size/2)), val)
        #self.set(-int(abs(size/2)), -int(abs(size/2)), val)
        pass

    def asArray(self):
        x_dif = abs(self.xMin - self.xMax) + 1
        z_dif = abs(self.zMin - self.zMax) + 1
        ret_arr = [[None for i in range(z_dif)] for j in range(x_dif)]

        for z in range(self.zMin, self.zMax + 1):
            for x in range(self.xMin, self.xMax + 1):
                reg = self.get_val(x, z)
                
                x_idx = x - self.xMin
                z_idx = z - self.zMin

                ret_arr[x_idx][z_idx] = reg


        return ret_arr
    
    def val_list(self):
        vals = []
        for x in range(self.xMin, self.xMax + 1):
            for z in range(self.zMin, self.zMax + 1):
                reg = self.region_arr.get(x, {}).get(z, 0)
                vals.append(reg)
        return vals