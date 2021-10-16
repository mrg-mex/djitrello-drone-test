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

    def start_drone(self, take_off=True):
        self._drone.connect()
        if take_off:
            self._drone.takeoff()
        return self._drone.is_flying

    def start_camera(self):
        self._is_camera_on = True
        self.camera_show()

    def stop_camera(self):
        self._is_camera_on = False

    def camera_show(self):
        try:
            if self._drone.stream_on:
                self._drone.streamoff()
            self._drone.streamon()
            while self._is_camera_on:
                frame_read = self._drone.get_frame_read()
                single_frame = frame_read.frame
                frame_img = cv2.resize(single_frame, (self._iw, self._ih))
                cv2.imshow("video01", frame_img)
                cv2.waitKey(1)
            if not self._is_camera_on:
                if self._drone.stream_on:
                    self._drone.streamoff()
                cv2.destroyWindow("video01")
        except Exception as e:
            print(str(e))

    def test_drone(self, left=100, rotate=90, forward=100, land=True):
        if not self._drone.is_flying:
            self._drone.takeoff()
        self._drone.move_left(left)
        self._drone.rotate_clockwise(rotate)
        self._drone.rotate_counter_clockwise(rotate)
        self._drone.move_right(left)
        self._drone.move_forward(forward)
        self._drone.move_back(forward)
        if land:
            self._drone.land()


if __name__ == '__main__':
    dronectrl = DroneCtrl()
    dronectrl.start_drone(False)
    print('Drone activado: bateria:{}'.format(dronectrl.get_battery()))
    dronectrl.start_camera()
    dronectrl.test_drone(20, 90, 20, True)
    dronectrl.stop_camera()
