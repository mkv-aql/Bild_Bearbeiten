import cv2

#open image
img = cv2.imread('autoausfuellen/weiter.JPG', cv2.IMREAD_UNCHANGED)
#show image
cv2.imshow('Image', img)
#wait for key press
cv2.waitKey(0)


import pyautogui
import time
import keyboard
import random

def move():
    screen_width, screen_height = pyautogui.size()

    while not keyboard.is_pressed('q'):
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(4)

    print("stopped")

move()
