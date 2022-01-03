import cv2
import numpy as np
import utilities as utils
from arduino import holder

camera = cv2.VideoCapture(1)

mog = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

while camera.grab():

    success, frame = camera.read()
    # frame = frame[323:758, 0:1920] # region of interest 1080p 16:9
    frame = frame[300:590, 0:1080]  # region of interest 720p 4:3
    frame = cv2.medianBlur(frame, 15)
    framebw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, framet = cv2.threshold(framebw, 125, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # Thresholding using otsu

    framet = cv2.morphologyEx(framet, cv2.MORPH_OPEN, (
        5, 5))  # Remove survived noise and simplify objects (less inner contours and false contours)

    bgs = mog.apply(framet, learningRate=0.05)  # stop counting when an object is placed/removed

    if np.count_nonzero(bgs) > 300:
        continue

    frame2 = framet.copy()
    contours, hierarchy = cv2.findContours(frame2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # Find contours
    totalContours = 0
    br = [] # bounding rectangles
    for i in range(len(contours)):
        # if hierarchy[0][i][3] == ROOT_NODE and cv2.contourArea(contours[i]) > 50:
        if cv2.contourArea(contours[i]) > 125:  # Only external contours are useful for counting, small area are removed
            poly = cv2.approxPolyDP(contours[i], 5, True)
            if cv2.boundingRect(poly)[1] < 55 or cv2.boundingRect(poly)[0] > 825:  # skip unnecessary detections outside the roi
                continue
            br.append(cv2.boundingRect(poly))
            totalContours += 1
    for b in br:
        cv2.rectangle(frame, (b[0], b[1]), (b[0] + b[2], b[1] + b[3]), (255, 255, 0), 3)
        camera_position = utils.getPosition((b[0], b[1]), (b[0] + b[2], b[1] + b[3]))
        weight = utils.match_cam_ino(camera_position, holder)
        cv2.putText(frame, str(br.index(b) + 1) + ' ' + str(weight) + 'g', (b[0], b[1] - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        #cv2.putText(frame, str(camera_position), (b[0], b[1] - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow('Buzdolabi kamerasi', frame)
    cv2.imshow('warped', utils.warpImg(frame))
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break
    print('Total contours: ', totalContours)

camera.release()
