import signal
import time
import subprocess
import threading

from ApiRequest import ApiRequest, SystemState

apiRequest = ApiRequest()


def startup():
    apiRequest.login()

    print('JWT Token:', apiRequest.jwtToken)

    if apiRequest.jwtToken != "":
        return True
    else:
        return False


stop_flag = threading.Event()
popen_list = []


def stream_camera(camera):
    ffmpeg_command = [
        'ffmpeg',
        '-i', 'rtsp://' + camera.localIp + ':8554/mjpeg/1',
        '-pix_fmt', 'yuv420p',
        '-c:v', 'libx264',
        '-r', '30',
        '-b:v', '1000k',
        '-f', 'mpegts',
        'srt://192.168.1.32:40005'
    ]
    p = subprocess.Popen(ffmpeg_command)
    popen_list.append(p)
    camera.process = p
    p.wait()
    apiRequest.updateHubReceiveVideoStream(camera.cameraId, False)


if __name__ == "__main__":

    start = startup()

    if start:

        beg_time = time.time()
        checkDelay = 3

        status = SystemState()
        threads = []

        while True:
            # Check if the hub needs to start or end
            if (time.time() - beg_time) > checkDelay:
                beg_time = time.time()
                print("Check status")
                # Get the new system status
                status = apiRequest.getSystemState()
                # Check if the hub has a user and if the security system is turned on
                if status.deviceHasUser & status.sysState:
                    print("System is activated")
                    for camera in status.cameras:
                        print(camera.localIp)
                        # Check if the ESP32-Cam is transmitting and if the hub does not transmit the signal
                        if camera.transmitVideoStream and not camera.hubReceiveVideoStream:
                            apiRequest.updateHubReceiveVideoStream(camera.cameraId, True)
                            print("Activate")
                            t = threading.Thread(target=stream_camera, args=(camera,))
                            threads.append(t)
                            t.start()

                        # Stop stream_camera thread and ffmpeg process if the camera does not transmit anymore
                        elif not camera.transmitVideoStream and camera.hubReceiveVideoStream:
                            print("Deactivate")
                            apiRequest.updateHubReceiveVideoStream(camera.cameraId, False)
                            for t in threads:
                                if t.name == camera.localIp:
                                    t.join()
                                    threads.remove(t)
                            # End ffmpeg proces
                            camera.process.terminate()

                        elif camera.transmitVideoStream and camera.hubReceiveVideoStream:
                            print('Running')
                        else:
                            print('Not Running')

                else:
                    print("Off")
                    print(len(threads))
                    # Close ffmpeg threads
                    if len(threads) > 0:
                        for t in threads:
                            t.join()
                    # Update the hub receive video to false in the database and stop the execution of the ffmpeg process
                    for camera in status.cameras:
                        if camera.hubReceiveVideoStream:
                            apiRequest.updateHubReceiveVideoStream(camera.cameraId, False)

                    for p in popen_list:
                        # Send SIGTERM signal to ffmpeg process
                        p.send_signal(signal.SIGTERM)

                    threads = []
            time.sleep(3)
        print("Hello Belgium")
    else:
        print("Unable to authenticate")
