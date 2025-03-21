import cv2
import cvzone
from cvzone.ColorModule import ColorFinder
import numpy as np
import pandas as pd
import math
import sqlite3

conn = sqlite3.connect('test.db')
# conn.execute('''
# CREATE TABLE RESULT  
# (
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     VIDNAME TEXT NOT NULL,
#     SUCCESS TEXT NOT NULL
# ); 
# ''')

videoLoc = "Videos/vid (5).mp4"
videoName = videoLoc.split("/")[1]
cap = cv2.VideoCapture(videoLoc)
myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 0, 'smin': 60, 'vmin': 181, 'hmax': 102, 'smax': 255, 'vmax': 255}
 
posListX = []
posListY = []
 
listX = [item for item in range(0,1920)]
start = True
prediction = False
flag = False
key = ""
 
while key != "n":
 
    if start:
        if len(posListX) == 10: start = False
        success, img = cap.read()
        # img = cv2.imread('Ball.png')
 
 
        img = img[0:900, :]
        imgPrediction = img.copy()
        imgResult = img.copy()
        imgBall, mask = myColorFinder.update(img, hsvVals)
        imgCon, contours = cvzone.findContours(img, mask, 200)
        if contours:
            posListX.append(contours[0]['center'][0])
            posListY.append(contours[0]['center'][1])
 
        if posListX:
            if len(posListX) < 18:
                coff = np.polyfit(posListX, posListY, 2)
            for i, (posX, posY) in enumerate(zip(posListX, posListY)):
                pos = (posX, posY)
                cv2.circle(imgCon, pos, 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(imgResult, pos, 10, (0, 255, 0), cv2.FILLED)
 
                if i == 0:
                    cv2.line(imgCon, pos, pos, (0, 255, 0), 2)
                    cv2.line(imgResult, pos, pos, (0, 255, 0), 2)
                else:
                    cv2.line(imgCon, (posListX[i - 1], posListY[i - 1]), pos, (0, 255, 0), 2)
                    cv2.line(imgResult, (posListX[i - 1], posListY[i - 1]), pos, (0, 255, 0), 2)
 
            for x in listX:
                y = int(coff[0] * x ** 2 + coff[1] * x + coff[2])
                cv2.circle(imgPrediction, (x, y), 2, (255, 0, 255), cv2.FILLED)
                cv2.circle(imgResult, (x, y), 2, (255, 0, 255), cv2.FILLED)
 
            # Predict
            if len(posListX) < 10:
                # y = int(coff[0] * x ** 2 + coff[1] * x + coff[2])
                a, b, c = coff
                c = c - 593
                x = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
                prediction = 300 < x < 430
            if prediction:
                flag = True 
                cvzone.putTextRect(imgResult, "Basket", (50, 150), colorR=(0, 200, 0),
                                   scale=5, thickness=10, offset=20)
            else:
                # conn.execute(f"INSERT INTO RESULT (VIDNAME,SUCCESS) VALUES ('f','NO')")
                # conn.commit()
                cvzone.putTextRect(imgResult, "No Basket", (50, 150), colorR=(0, 0, 200),
                                   scale=5, thickness=10, offset=20)
 
        cv2.line(imgCon, (330, 593), (430, 593), (255, 0, 255), 10)
        imgResult = cv2.resize(imgResult, (0, 0), None, 0.7, 0.7)
        # imgStacked = cvzone.stackImages([img,imgCon,imgPrediction,imgResult],2,0.35)
 
        cv2.imshow("imgCon", imgResult)
    
    key = cv2.waitKey(100)
    if key == ord("s"):
        start = True
    if key == ord("n"):
        key = "n"


entryFlag = False
resultQuery = conn.execute("SELECT VIDNAME FROM RESULT")

if resultQuery.rowcount == -1:
    entryFlag = True
for row in resultQuery:
    print(row)
    for val in row:
        if val != videoName:        
            entryFlag = True
        else:
            entryFlag = False
            print("already present")
            break

if flag==True and entryFlag == True:
            conn.execute(f"INSERT INTO RESULT (VIDNAME,SUCCESS) VALUES (?,?)",[videoName,"YES"])
            conn.commit()
if flag==False and entryFlag == True:
            conn.execute(f"INSERT INTO RESULT (VIDNAME,SUCCESS) VALUES (?,?)",[videoName,"NO"])
            conn.commit()

def getExcel():
   sql_query = '''SELECT DISTINCT * from RESULT'''
   sql_query = pd.read_sql_query(sql_query,conn)
   df = pd.DataFrame(sql_query)
   try:
        with pd.ExcelWriter('output.xlsx',
                            mode='w') as writer:
                df.to_excel(writer,index=False)
   except (FileNotFoundError):
        df.to_excel("output.xlsx",index=False)

    
getExcel()

