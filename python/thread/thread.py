import multiprocessing
import time
import sys
sys.path.insert(0, '../i2c')
from imu import run_imu
from oled import write_oled
accgyro = multiprocessing.Array('i', 6)

if __name__ == "__main__":
    number = 7
    result = None

lock = multiprocessing.Lock()
p1 = multiprocessing.Process(target=run_imu, args=(accgyro, lock))
p2 = multiprocessing.Process(
    target=write_oled, args=(','.join([str(accgyro[i]) for i in accgyro]), lock))
p1.start()
p2.start()
p1.join()
p2.join()

# Wont print because processes run using their own memory location
print(result)
