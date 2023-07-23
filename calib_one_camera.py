import configparser
import cv2
import numpy as np
import os


class OneCameraCalibration:

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.optionxform = str
        self._R = []
        self._t = []

    def get_calibration(self, folder, string):
        CHECKERBOARD = (10, 6)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.

        objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
        objp *= 4
        for filename in os.listdir(folder):
            if filename.endswith(".jpeg"):  # you may specify other image formats
                img_path = os.path.join(folder, filename)
                img = cv2.imread(img_path)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

                # If found, add object points, image points (after refining them)
                if ret:
                    objpoints.append(objp)
                    corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                    imgpoints.append(corners)

                    # Draw and display the corners
                    cv2.drawChessboardCorners(img, (7, 6), corners2, ret)
                    cv2.imshow('img', img)
                    cv2.waitKey(500)

        cv2.destroyAllWindows()

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints,
                                                           imgpoints,
                                                           gray.shape[::-1],
                                                           None,
                                                           None)
        print(mtx)
        print()
        print(dist)
        self._config[string] = {}
        self._config[string]['fx'] = str(mtx[0, 0])
        self._config[string]['fy'] = str(mtx[1, 1])
        self._config[string]['cx'] = str(mtx[0, 2])
        self._config[string]['cy'] = str(mtx[1, 2])
        self._config[string]['k1'] = str(dist[0][0])
        self._config[string]['k2'] = str(dist[0][1])
        self._config[string]['p1'] = str(dist[0][2])
        self._config[string]['p2'] = str(dist[0][3])
        self._config[string]['k3'] = str(dist[0][4])

        with open("left_camera_config.conf", 'w') as configfile:
            self._config.write(configfile)
        return mtx


def main():
    calibration = OneCameraCalibration()

    k1 = calibration.get_calibration("left", "LEFT_CAM_FHD")
    print(k1)


if __name__ == "__main__":
    main()
