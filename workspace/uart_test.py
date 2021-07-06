from machine import UART
import time
import uos
u = UART(0,115200)
u.init(115200, bits=8, parity=None, stop=1)

u.write("\nstart  \n")
dir = uos.listdir()
for str in dir :
    u.write(str)
    u.write('  \n')
    time.sleep(0.2)  



