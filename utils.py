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

videoLoc = "Videos/vid 4.mp4"
videoName = videoLoc.split("/")[1]
cap = cv2.VideoCapture(videoLoc)


myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 0, 'smin': 60, 'vmin': 181, 'hmax': 102, 'smax': 255, 'vmax': 255}

# Variables

posListX,posListY = [],[]
xList = [item for item in range(0,1920)]
start = True
prediction = False
flag = False
key = ""

while key != "n":
    if start:
        if len(posListX) == 8: start = False
        success, img = cap.read()           
        # img = cv2.imread("Ball2.png")
        img = img[0:900,140:]

            #Find the ball's color
        imgColor,mask = myColorFinder.update(img,hsvVals)
            
            #Find location of the Ball
        imgContours,contours = cvzone.findContours(img, mask, minArea=1000)
            
        if contours:
            posListX.append(contours[0]['center'][0])
            posListY.append(contours[0]['center'][1])

        if posListX:
            #Polynomial Regression y = ax^2 + bx + c
            #Find the coeffecients
            A,B,C = np.polyfit(posListX,posListY,2)


            for i,(posX,posY) in enumerate(zip(posListX,posListY)): 
                pos = (posX,posY)       
                cv2.circle(imgContours,pos,15,(0,255,0),cv2.FILLED)
                if i==0:
                    cv2.line(imgContours,pos,pos,(0,255,0),4)
                else:
                    cv2.line(imgContours,pos,(posListX[i - 1],posListY[i-1]),(0,255,0),4)

            for x in xList:
                    y = int(A*x**2 + B*x + C)  
                    cv2.circle(imgContours,(x,y),3,(255,255,0),cv2.FILLED)

                #Prediction
                # X values from 200 to 400 Y 530
            if len(posListX) < 8: 
                a = A
                b = B
                c = C - 430
                x = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
                prediction = 227 < x < 400

            if prediction:
                    cvzone.putTextRect(imgContours,"Basket",(50,100),scale=7,thickness=5,colorR=(0,200,0))
            else:
                    cvzone.putTextRect(imgContours,"No Basket",(50,100),scale=7,thickness=5,colorR=(0,0,200))
            #Display
            img = cv2.resize(img, (0,0),None,0.7,0.7)
            imgContours = cv2.resize(imgContours, (0,0),None,0.7,0.7)
            cv2.imshow("ImageColor",imgContours)

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