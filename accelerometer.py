import board
from adafruit_lis3dh import LIS3DH_I2C

class Accelerometer():
    def __init__(self):
        i2c = board.I2C()
        self.lis3dh = LIS3DH_I2C(i2c, address=0x19)

    @property
    def portrait(self):
        rotation = self.rotation
        return True if rotation == 0 or rotation == 180 else False;

    @property
    def landscape(self):
        rotation = self.rotation
        return True if rotation == 90 or rotation == 270 else False;

    @property
    def rotation(self):
        #  To me, it seems like the x/y values are messed up.
        #  These are different than other values in example
        #  code.  But this works for the MagTag...
        x, y, z = self.lis3dh.acceleration
        if abs(x) < abs(y):
            if y > 0:
                return 270
            else:
                return 90
        else:
            if x > 0:
                return 180
            else:
                return 0
        return 0