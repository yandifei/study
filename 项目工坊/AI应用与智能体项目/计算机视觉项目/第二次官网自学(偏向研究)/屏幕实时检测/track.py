from time import sleep

from ultralytics import YOLO
import cv2 as cv
import pyautogui as pg
import numpy as np


model = YOLO("v26 600(屏幕微信和qq).pt")



while True:
    if cv.waitKey(1) == ord('q'):
        break
    shot = pg.screenshot()
    shot_np = np.array(shot)
    shot_np = shot_np[:, :, ::-1]
    # cv.imshow('screen', shot)
    result = model.track(shot_np, show=True, persist=True)
    # result = model.track(source="screen", show=True)
    # print(result)
    for i in result[0].boxes.xywh:
        print(i)
        # pg.moveTo(i[0], i[1])
    # sleep(1)


cv.waitKey(0)
cv.destroyAllWindows()