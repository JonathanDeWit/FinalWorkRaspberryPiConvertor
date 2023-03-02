import requests
import json
import csv


class ApiRequest:
    def __init__(self):
        self.apiUrl = ""
        self.hubPath = ""
        self.userName = "null"
        self.apiPassword = "null"

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

    def helloWorld(self):
        # simple get request
        response = requests.get('https://finalworkapi.azurewebsites.net/api/user/helloworld')
        print(response.text)

    def login(self):
        # Get request with a json body with the username and password of the raspberry pi
        url = 'https://finalworkapi.azurewebsites.net/api/hubuser/login'
        payload = {"Email": self.userName, "Password": self.apiPassword}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        jwtToken = "null"
        if response.status_code == 200:
            json_response = response.json()
            jwtToken = json_response.get('jwtToken')
            return jwtToken
        else:
            print('Request failed with status code', response.status_code)
            return jwtToken

    def updateHubReceiveVideoStream(self, jwt_token="", camera_id=0, status=True):
        headers = {"Authorization": "Bearer " + jwt_token}
        response = requests.post(self.apiUrl + self.hubPath + "/update/UpdateHubReceiveVideoStream?cameraId=" + str(
            camera_id) + "&hubReceiveVideoStream=" + str(status), headers=headers)

        if response.status_code == 200:
            print(response.text)
            return True
        else:
            print('Request failed with status code', response.status_code)
            return False

    def getSystemState(self, jwt_token=""):
        headers = {"Authorization": "Bearer " + jwt_token}
        response = requests.get(self.apiUrl + self.hubPath + "/getSystemState", headers=headers)

        status = SystemState()

        if response.status_code == 200:
            json_response = response.json()
            status.sys_state = json_response.get('SysState')
            status.deviceHasUser = json_response.get('DeviceHasUser')

            for camera in json_response.get('Cameras'):
                cameraObject = Camera(camera["CameraId"], camera["LocalIp"], camera["TransmitVideoStream"],
                                      camera["HubReceiveVideoStream"])
                status.cameras.append(cameraObject)
        else:
            print('Request failed with status code', response.status_code)

        return status


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

    def __init__(self, camera_id, local_ip, transmit_video_stream, hub_receive_video_stream):
        self.cameraId = camera_id
        self.localIp = local_ip
        self.transmitVideoStream = transmit_video_stream
        self.hubReceiveVideoStream = hub_receive_video_stream
