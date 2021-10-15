# Control del drone Dji Trello
import cv2
from djitellopy import Tello


class DroneCtrl:
    def __init__(self, image_width=320, image_height=240):
        self._iw = image_width
        self._ih = image_height
        self._drone = Tello()
        self._is_camera_on = False

    def get_battery(self):
        # Get drone's battery charge level.
        return self._drone.get_battery()

    def get_speed(self):
        return self._drone.get_speed_x(), self._drone.get_speed_y(), self._drone.get_speed_z()

    def get_orientation(self):
        return self._drone.get_yaw(), self._drone.get_pitch(), self._drone.get_roll()

    def get_state(self):
        return self._drone.get_current_state()

    def start_drone(self):
        self._drone.connect()
        self._drone.for_back_velocity = 0
        self._drone.left_right_velocity = 0
        self._drone.up_down_velocity = 0
        self._drone.yaw_velocity = 0
        self._drone.speed = 0

    def start_camera(self):
        self._is_camera_on = True
        self.camera_show()

    def stop_camera(self):
        self._is_camera_on = False

    def camera_show(self):
        while self._is_camera_on:
            frame_read = self._drone.get_frame_read()
            frame_img = cv2.resize(frame_read.frame, (self._iw, self._ih))
            cv2.imshow('Drone video feed', frame_img)

        # cv2.destroyWindow('Drone video feed')
        cv2.destroyAllWindows()


if __name__ == '__main__':
    dronectrl = DroneCtrl(640, 480)
    dronectrl.start_drone()
    print('Drone activado: bateria:{}, {}'.format(dronectrl.get_battery(), dronectrl.get_state()))
    dronectrl.start_camera()

