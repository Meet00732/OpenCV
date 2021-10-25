import cv2
import numpy as np
import pyautogui as pag
import HandTrackingModule as htm
import time


camWidth = 640
camHeigth = 480

cap = cv2.VideoCapture(0)
cap.set(3, camWidth)
cap.set(4, camHeigth)

detector = htm.Hand_Detector(min_detection_confidence=0.75, min_tracking_confidence=0.5, max_hands=1)

#variables
cTime = 0
pTime = 0
smooth = 1
FrameR = 100
clocX, clocY = 0, 0
plocX, plocY = 0, 0

scrWidth, scrHeight = pag.size()
pag.FAILSAFE = False

while (cap.isOpened()):
    frame, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, Draw=False)
    if len(lmList) != 0:
        # print(lmList)

        Fingers = detector.fingerCount(lmList)
        # print(Fingers)

        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        #Rectangle boundry
        cv2.rectangle(img, (FrameR, FrameR), (camWidth - FrameR, camHeigth - FrameR), (0, 255, 0), 2)

        if Fingers[1] == 1 and Fingers[0] == 1 and Fingers[2] == 1:
            #Change Coordinates according to the screen
            newX = np.interp(x1, [FrameR, camWidth - FrameR], [0, scrWidth])
            newY = np.interp(y1, [FrameR, camHeigth - FrameR], [0, scrHeight])

            #Smooth the movement of mouse
            clocX = plocX + (newX - plocX) / smooth
            clocY = plocY + (newY - plocY) / smooth

            #Move the Mouse to the clocX, clocY pos
            pag.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY

        if Fingers[1] == 1 and Fingers[0] == 0 and Fingers[2] == 1:
            pag.click()
            pag.PAUSE = 0.2

        if Fingers[1] == 1 and Fingers[0] == 1 and Fingers[2] == 0:
            pag.doubleClick()
            pag.PAUSE = 0.2

    cTime = time.time()
    t = cTime - pTime
    if t != 0:
        fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    cv2.imshow("img", img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()