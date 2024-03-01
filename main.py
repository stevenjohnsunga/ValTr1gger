import cv2
import numpy as np
import pyautogui
import win32api
import mss
import time
from random import randint
import keyboard


COMPORT_NUMBER = 3
X_FOV = 28
Y_FOV = 28
X_SPEED = int(4)
Y_SPEED = 3
AIMING_PRECISION = int(6)
TRIGGERBOT_X_SIZE = 3
TRIGGERBOT_Y_SIZE = 25
AIM_KEYS = [0x01]
TRIGGER_KEYS = [0x12, 0x05]
TOGGLE_MODE = False 


LOWER_COLOR = [130,50,195]
UPPER_COLOR = [150,255,255]
KERNEL_SIZE = (3, 3)
DILATING = 3
DEBUGGING = False 
print("version 1.4 always")
def themagicpress():
    keyboard.press('k')
    time.sleep(.2)
    keyboard.release('k')


while True:
    if (True):
        monitor_size = pyautogui.size()
        x_center = monitor_size.width // 2
        y_center = monitor_size.height // 2
        left = x_center - X_FOV // 2
        top = y_center - Y_FOV // 2
        region = {'left': left, 'top': top, 'width': X_FOV, 'height': Y_FOV}

        with mss.mss() as sct:
            screenshot = sct.grab(region)
            screen_array = np.array(screenshot)

        hsv = cv2.cvtColor(screen_array, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array(LOWER_COLOR), np.array(UPPER_COLOR))
        kernel = np.ones(KERNEL_SIZE, np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=DILATING)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contours:
            screen_center = (X_FOV // 2, Y_FOV // 2)
            min_distance = float('inf')
            closest_contour = None

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                distance = ((center[0] - screen_center[0]) ** 2 + (center[1] - screen_center[1]) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour

            x, y, w, h = cv2.boundingRect(closest_contour)
            cX = x + w // 2
            cY = y + h // 2
            top_most_y = y + AIMING_PRECISION

            x_offset = cX - screen_center[0]
            y_offset = top_most_y - screen_center[1]
            trigger_y_offset = cY - screen_center[1]
            if abs(x_offset) <= TRIGGERBOT_X_SIZE and abs(trigger_y_offset) <= TRIGGERBOT_Y_SIZE:
                time.sleep(0.020) #human
                themagicpress()
