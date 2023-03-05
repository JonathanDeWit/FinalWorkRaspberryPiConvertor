import requests
import json
import csv
import time


class ApiRequest:
    def __init__(self):
        self.apiUrl = ""
        self.hubPath = ""
        self.userName = "null"
        self.apiPassword = "null"
        self.jwtToken = ""
        self.tokenCreationTime = time.time()
        self.tokenValidationTime = 3600

        # Open CSV and import api url, username and password
        with open('conf.csv', mode='r') as file:
            # read CSV conf file
            reader = csv.reader(file)
            row = next(reader)
            # extract the username and password from the row
            self.apiUrl = row[0]
            self.hubPath = row[1]
        with open('profile.csv', mode='r') as file:
            # read CSV conf file
            reader = csv.reader(file)
            row = next(reader)
            # extract the username and password from the row
            self.userName = row[0]
            self.apiPassword = row[1]

    def checkTokenValidation(self):

        if (time.time() - self.tokenCreationTime) < self.tokenValidationTime:
            return True
        else:
            return False

    def login(self):
        # Get request with a json body with the username and password of the raspberry pi
        url = 'https://finalworkapi.azurewebsites.net/api/hubuser/login'
        payload = {"Email": self.userName, "Password": self.apiPassword}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        jwtToken = "null"
        if response.status_code == 200:
            json_response = response.json()
            self.jwtToken = json_response.get('jwtToken')
            self.tokenCreationTime = time.time()
            return self.jwtToken
        else:
            print('Request failed with status code', response.status_code)
            return jwtToken

    def updateHubReceiveVideoStream(self, camera_id=0, status=True):
        if self.checkTokenValidation():
            headers = {"Authorization": "Bearer " + self.jwtToken}
            response = requests.post(self.apiUrl + self.hubPath + "/update/UpdateHubReceiveVideoStream?cameraId=" + str(
                camera_id) + "&hubReceiveVideoStream=" + str(status), headers=headers)

            if response.status_code == 200:
                print(response.text)
                return True
            else:
                print('Request failed with status code', response.status_code)
                return False
        else:
            self.login()

    def getSystemState(self):
        if self.checkTokenValidation():
            headers = {"Authorization": "Bearer " + self.jwtToken}
            response = requests.get(self.apiUrl + self.hubPath + "/getSystemState", headers=headers)

            status = SystemState()

            if response.status_code == 200:
                json_response = response.json()
                print(json_response)
                status.sysState = json_response.get('SysState')
                status.deviceHasUser = json_response.get('DeviceHasUser')

                for camera in json_response.get('Cameras'):
                    cameraObject = Camera(camera["CameraId"], camera["LocalIp"], camera["TransmitVideoStream"],
                                          camera["HubReceiveVideoStream"], camera["SrtServerIp"], camera["SrtServerPort"])
                    status.cameras.append(cameraObject)
            else:
                print('Request failed with status code', response.status_code)

            return status
        else:
            self.login()


class SystemState:

    def __init__(self, sys_state, device_has_user, cameras):
        self.sysState = sys_state
        self.diviceHasUser = device_has_user
        self.cameras = cameras

    def __init__(self):
        self.sysState = False
        self.deviceHasUser = False
        self.cameras = []


class Camera:
    cameraId = 1
    localIp = ""
    transmitVideoStream = False
    hubReceiveVideoStream = False
    srtServerIp = "0.0.0.0"
    srtServerPort = 0

    def __init__(self, camera_id, local_ip, transmit_video_stream, hub_receive_video_stream, srt_server_ip, srt_server_port):
        self.cameraId = camera_id
        self.localIp = local_ip
        self.transmitVideoStream = transmit_video_stream
        self.hubReceiveVideoStream = hub_receive_video_stream
        self.srtServerIp = srt_server_ip
        self.srtServerPort = srt_server_port
