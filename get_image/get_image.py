# Author: Qingyu WANG
# Contact: 120153710@qq.com
# Date: 03 Feb. 2021
# Usage: for testing the easy image from CoppeliaSim via python remoteApi
import sys
sys.path.append('python')
import numpy as np
import cv2
print('Program started')
try:
    import sim as vrep
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')
print('Program started')
vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
if clientID != -1:
    print('Connected to remote API server!')
    res, v0 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    res, resolution, imag = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_streaming)
    imcount = 0
    while (vrep.simxGetConnectionId(clientID) != -1):
        res, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
        if res == vrep.simx_return_ok:
            imcount = imcount + 1
            res, rgb_resolution, rgb_image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
            rgb_img = np.array(rgb_image, dtype=np.uint8)
            rgb_img.resize([rgb_resolution[1], rgb_resolution[0], 3])
            rgb_img = cv2.flip(rgb_img, 0)
            cv2.imshow("RGB_Image", rgb_img)
            vrep.simxAddStatusbarMessage(clientID, 'hello world', vrep.simx_opmode_oneshot)
            cv2.waitKey(1)
            print(imcount)
        else:
            print('Failed to show rgb and depth image')
else:
    print('Failed to connect to vrep API server!')
print('Program ended!')
