import time
import cv2

import pithermalcam as ptc
# from pithermalcam.pi_therm_cam import pithermalcam
from pithermalcam2.modded_pi_therm_cam import pithermalcam


if __name__ == "__main__":
    #ptc.test_camera()
    # ptc.display_camera_live()
    output_folder = "/home/trueshot/thermalcam_ws/src/MLX90640_python"
    thermcam = pithermalcam(output_folder=output_folder)  # Instantiate class
    thermcam.display_camera_onscreen()
    #cam = pithermalcam()
    # while True:
    #cam_data = cam.update_image_frame()
    #print(cam_data)

    #cv2.namedWindow('Thermal Image', cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('Thermal Image', 1200, 900)
    #cv2.imshow('Thermal Image', cam_data)
    #cv2.waitKey(0)
