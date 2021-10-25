import cv2
import time
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

hcam = 2048
wcam = 1024

#down - 50
#mid - 200
#top - 350

cam = cv2.VideoCapture(0)
cam.set(3, wcam)
cam.set(4, hcam)
pTime = 0
cTime = 0

detector = htm.Hand_Detector(min_detection_confidence=0.75, min_tracking_confidence=0.5)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# print(volume.GetMasterVolumeLevel())
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20.0, None)
minVol = volRange[0]
maxVol = volRange[1]
# print(minVol)
# print(maxVol)
# print(volRange)
vol = 0
volBar = 400
volPer = 0

while True:
    frame, img = cam.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmlist = detector.findPosition(img, Draw=False)
    if len(lmlist) != 0:
        # print(lmlist[8][2])
        y = lmlist[8][2]
        Fingers = detector.fingerCount(lmlist)
        vol = np.interp(y, [150, 400], [maxVol, minVol])
        volBar = np.interp(y, [150, 400], [130, 400])
        volPer = np.interp(y, [150, 400], [100, 0])
        # print(volPer)
        # print(y, vol)
        volume.SetMasterVolumeLevel(vol, None)

    cv2.line(img, (480, 130), (840, 130), (0, 255, 0), 3)
    # cv2.line(img, (480, 230), (840, 230), (255, 0, 0), 3)
    cv2.line(img, (480, 400), (840, 400), (0, 0, 255), 3)

    cv2.rectangle(img, (50, 130), (85, 400), (0, 0, 0), 3)



    if int(volPer) > 70:
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, (str(int(volPer)) + "%"), (45, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    else:
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, (str(int(volPer)) + "%"), (45, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0 , 255, 0), 3)

    #range = 50-350
    #vol = -65-0




    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    # img = img.flip()
    cv2.imshow("image", img)
    if cv2.waitKey(1) == ord('q'):
        break
