# Author: Qingyu WANG
# Contact: 120153710@qq.com
# Date: 03 Feb. 2021
# Usage: for testing the easy image from CoppeliaSim via python remoteApi
import sys
import math
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

baseName = 'UR5'
jointName = 'UR5_joint'
jointNum = 6
RAD2DEG = 180 / math.pi
jointHandle = np.zeros((jointNum,), dtype=np.int)
jointConfig = np.zeros((jointNum,))

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
vrep.simxSetFloatingParameter(clientID, vrep.sim_floatparam_simulation_time_step, 0.005, vrep.simx_opmode_oneshot)
vrep.simxSynchronous(clientID, True)
vrep.simxStartSimulation(clientID, vrep.simx_opmode_oneshot)
if clientID != -1:
    print('Connected to remote API server!')
    # res, consoleOpen_handle = vrep.simxAuxiliaryConsoleOpen(clientID, 'hello', 3, 0b00100, None, None, None, None, vrep.simx_opmode_oneshot)

    for i in range(jointNum):
        _, returnHandle = vrep.simxGetObjectHandle(clientID, jointName + str(i+1), vrep.simx_opmode_blocking)
        jointHandle[i] = returnHandle
    _, baseHandle = vrep.simxGetObjectHandle(clientID, baseName, vrep.simx_opmode_blocking)
    _, gripperHandle = vrep.simxGetObjectHandle(clientID, 'RG2_openCloseJoint', vrep.simx_opmode_blocking)

    for i in range(jointNum):
        _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)
        jointConfig[i] = jpos
        print(jointConfig[i])
    _, gpos = vrep.simxGetJointPosition(clientID, gripperHandle, vrep.simx_opmode_blocking)
    print(gpos)

    vrep.simxPauseCommunication(clientID, True)
    vrep.simxSetJointTargetPosition(clientID, jointHandle[3], 120/RAD2DEG, vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetPosition(clientID, gripperHandle, 0, vrep.simx_opmode_oneshot)
    vrep.simxPauseCommunication(clientID, False)

    for i in range(jointNum):
        _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_blocking)
        jointConfig[i] = jpos
        print(jointConfig[i])
    _, gpos = vrep.simxGetJointPosition(clientID, gripperHandle, vrep.simx_opmode_blocking)
    print(gpos)

else:
    print('Failed to connect to vrep API server!')
print('Program ended!')
