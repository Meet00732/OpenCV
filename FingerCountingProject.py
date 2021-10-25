import cv2
import time
import os
import HandTrackingModule as htm

wcam = 720
hcam = 640

cap = cv2.VideoCapture(0)

cap.set(3, wcam)
cap.set(4, hcam)

folderPath = "finger_images"
myList = os.listdir(folderPath)
# print(myList)
OverlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    image = cv2.resize(image, (200, 200))
    OverlayList.append(image)

print(len(OverlayList))


detector = htm.Hand_Detector(min_detection_confidence=0.75, min_tracking_confidence=0.4)

cTime = 0
pTime = 0
lmList = []
tipId = [4, 8, 12, 16, 20]
Counter = 0



while True:
    frame, img = cap.read()
    img = cv2.flip(img, 1)
    # cv2.namedWindow("image", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    totalFinger = 0
    # OverLay Images

    # OverlayList[0].resize(200, 200)
    # img[0:200, 0: 200] = OverlayList[1]

    img = detector.findHands(img)
    lmList = detector.findPosition(img, Draw=False)

    if len(lmList) != 0:
        # print(lmList[4], lmList[2])
        Finger = []
        if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:
            Finger.append(1)
        else:
            Finger.append(0)


        for id in range(1, 5):
            if lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]:
                Finger.append(1)
            else:
                Finger.append(0)

        # print(Finger)
            totalFinger = Finger.count(1)
        print(totalFinger)


    cTime = time.time()
    t = cTime - pTime
    if t != 0:
        fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.rectangle(img, (10, 80), (140, 180), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, str(totalFinger), (60, 140), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    cv2.putText(img,f'FPS: ' + str(int(fps)), (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("image", img)
    if cv2.waitKey(1) == ord('q'):
        break
