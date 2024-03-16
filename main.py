# pip install cmake (at local)
# pip install boost (at local)
"""
git clone https://github.com/davisking/dlib.git
cd dlib
python setup.py install 
"""  # (At git bash)

import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # (width)
cap.set(4, 480)  # (height)

imgBackground = cv2.imread("Resources/background.png")


# Read all the mode images and store them in a list
folderModePath = 'Resources/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
	imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# load the encoding file
print("loading Encoding File ...")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
print("Encoding File Loaded")


while True:
	success, img = cap.read()

	imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
	imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

	faceCurFrame = face_recognition.face_locations(imgS)
	encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

	imgBackground[139:139 + 480, 93:93 + 640] = img  # (height, width)
	imgBackground[139:139 + 480, 752:752 + 414] = imgModeList[0]

	for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
		matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
		faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

		print("matches", matches)
		print("faceDis",  faceDis)

		matchIndex = np.argmin(faceDis)
		print("MatchIndex", matchIndex)

		if matches[matchIndex]:

			studentId = studentIds[matchIndex]
			y1, x2, y2, x1 = faceLoc
			y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
			bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
			imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
			cv2.putText(imgBackground, studentId, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

	# cv2.imshow("Webcam", img)
	cv2.imshow("Face Attendance", imgBackground)
	cv2.waitKey(1)
