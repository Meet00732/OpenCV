import cv2
import mediapipe as mp

class Hand_Detector:
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipId = [4, 8, 12, 16, 20]


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, HandNo=0, Draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[HandNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if Draw:
                    cv2.circle(img, (cx, cy), 15, (255, 255, 0), cv2.FILLED)

        return lmList

    def fingerCount(self, lmList):
        Finger = []
        if lmList[self.tipId[0]][1] > lmList[self.tipId[0] - 1][1]:
            Finger.append(1)
        else:
            Finger.append(0)

        for id in range(1, 5):
            if lmList[self.tipId[id]][2] < lmList[self.tipId[id] - 2][2]:
                Finger.append(1)
            else:
                Finger.append(0)

        return Finger
