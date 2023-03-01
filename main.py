import subprocess
import requests
import json

if __name__ == "__main__":

    #simple get request
    response = requests.get('https://finalworkapi.azurewebsites.net/api/user/helloworld')
    print(response.text)



    # get request with a json body
    url = 'https://finalworkapi.azurewebsites.net/api/hubuser/login'
    payload = {"Email": "HubA", "Password": "Jonathan01429"}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    jwt_token = ""
    if response.status_code == 200:
        json_response = response.json()
        jwt_token = json_response.get('jwtToken')
        print('JWT Token:', jwt_token)
    else:
        print('Request failed with status code', response.status_code)
    


    # get request with a jwt token
    url = 'https://finalworkapi.azurewebsites.net/api/hubuser/getSystemState'
    headers = {"Authorization": "Bearer "+jwt_token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_response = response.json()
        print(json.dumps(json_response, indent=2))
    else:
        print('Request failed with status code', response.status_code)

    # # Define the ffmpeg command as a list of strings
    # ffmpeg_command = [
    #     'ffmpeg',
    #     '-i', 'rtsp://192.168.1.28:8554/mjpeg/1',
    #     '-pix_fmt', 'yuv420p',
    #     '-c:v', 'libx264',
    #     '-r', '30',
    #     '-b:v', '1000k',
    #     '-f', 'mpegts',
    #     'srt://192.168.1.32:40005'
    # ]
    #
    # # Use the subprocess module to execute the command
    # subprocess.call(ffmpeg_command)

    print("Hello Belgium")
