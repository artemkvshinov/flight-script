from pioneer_sdk import Pioneer, Camera
import numpy as np
import time
import cv2

def main():
    pioneer_mini = Pioneer()
    camera = Camera()
    flag = 0

    # Dictionary of aruco-markers
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
    # Parameters for marker detection (in this case, default parameters)
    aruco_params = cv2.aruco.DetectorParameters()
    # Create instance of ArucoDetector.
    # Required starting from version opencv 4.7.0
    aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    try:
        while True:
            key = cv2.waitKey(1)
            if key == ord('s'):
                if flag == 0:
                    flag = 1
                    pioneer_mini.arm()
                    pioneer_mini.takeoff()
                    time.sleep(0.25)
                    pioneer_mini.go_to_local_point(0, 0, 1, 0)
                    time.sleep(1)

                elif flag  == 1:
                    flag = 0
                    pioneer_mini.land()
                    time.sleep(1)
                print(flag)

            elif key == 27:  # esc
                    cv2.destroyAllWindows()
                    pioneer_mini.land()
                    pioneer_mini.close_connection()
                    del pioneer_mini
                    break

            frame = camera.get_frame()
            if frame is not None:
                camera_frame = cv2.imdecode(
                    np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR
                )
                cv2.imshow("pioneer_camera_stream", camera_frame)

            # Detect markers
            corners, ids, rejected = aruco_detector.detectMarkers(frame)
            # Highlight the decoded markers on the image
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            cv2.imshow("video", frame)  # Show an image on the screenc

    finally:
        pioneer_mini = Pioneer()
        time.sleep(1)
        pioneer_mini.land()

        pioneer_mini.close_connection()
        del pioneer_mini


if __name__ == '__main__':
    main()
