import subprocess
import requests
import json
import csv

from ApiRequest import ApiRequest

if __name__ == "__main__":

    apiRequest = ApiRequest()
    apiRequest.helloWorld()

    jwtToken = apiRequest.login()

    print('JWT Token:', jwtToken)

    status = apiRequest.getSystemState(jwtToken)

    for camera in status.cameras:
        print(camera.cameraId)
        apiRequest.updateHubReceiveVideoStream(jwtToken, camera.cameraId, True)

    status = apiRequest.getSystemState(jwtToken)
    for camera in status.cameras:
        print(str(camera.hubReceiveVideoStream))

    print("Hello Belgium")
