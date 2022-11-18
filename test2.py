import os
from datetime import datetime
from datetime import date
import datetime as d
import numpy as np
import cv2
import face_recognition
import mysql.connector
from PIL import Image
import io

today=date.today()
mydb = mysql.connector.connect(
  host="10.147.18.177",
  user="user",
  password="user@mysql"
)
mycursor = mydb.cursor()
mycursor.execute("use erp;")
images = []
classNames = []
stuid = []
classid = 0;
try:
    mycursor.execute("SELECT classid FROM camnodes WHERE ip = " + "\'10.147.18.204\' ;")
    classid = mycursor.fetchone()[0]
    mycursor.execute("SELECT id FROM student WHERE classid = " + str(classid) + " ;")
    studs = []
    for row in mycursor.fetchall():
        studs.append(row[0])
    for stu in studs:
        print(stu)
        mycursor.execute("SELECT name, photo, id FROM student WHERE id = " + str(stu) + ";")
        details = mycursor.fetchone()
        image = Image.open(io.BytesIO(details[1]))
        #image.show()
        cur = np.array(image)
        images.append(cur)
        classNames.append(details[0])
        stuid.append(details[2])
        print(classNames)
except Exception:
    print("blah")

# path = 'imgattendance'
# classNames2=[]
# myList = os.listdir(path)
# print(myList)
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     print(np.shape(curImg))
#     #print(curImg)
#     #xd0print(len(curImg))
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])
#     #classNames2.append(os.path.splitext())
#     #print(os.path.splitext(cl))
# print(classNames)
#
# for kk in classNames:
#     classNames2.append(kk.split('_')[0])
# print(classNames2)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        #print(encode)
        encodeList.append(encode)
    return encodeList


def markAttendance(id):
    # try:
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        idList = []
        for line in myDataList:
            entry = line.split(',')
            idList.append(entry[0])
        #print(str(id) not in idList)
        if str(id) not in idList:
            now = date.today()
            now = datetime.now().strftime("%H")
            print(now)
            f.writelines(f'{id},{now}\n')
        f.close()
    # except Exception:
    #     print("Cool")
#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)


st = datetime.now().minute;
t = st
while t < ((st+1)%60):
    success, img = cap.read()
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)



        if faceDis[matchIndex] < 0.55:
            name = classNames[matchIndex].upper()
            id = stuid[matchIndex]
            markAttendance(id)
        else:
            name = 'Unknown'
        # print(name)
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        #markAttendance(name)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
    t = datetime.now().minute
    print(t)
# try:
t = d.time(8,35,00)
print(t)
hi = ''.join([str(t.hour), str(t.minute), "00"])
cmd = "SELECT slot FROM `slots` WHERE start <= %s and end >= %s LIMIT 1;" % (hi, hi)
mycursor.execute(cmd)
slotid = mycursor.fetchone()[0]
mycursor.execute("SELECT %s FROM timetable WHERE day = %s AND classid = %s LIMIT 1"%(str("slot" + str(slotid)),str(int(datetime.now().weekday())+1),classid))
courseid = mycursor.fetchone()[0]
with open("Attendance.csv","r") as f:
    datalist = f.readlines()
    for line in datalist:
        data = line.split(',')
        print(data)
        id = data[0]
        #date = data[1].split('\n')[0]
        datevar = today.strftime('%y%m%d')
        print('hiiiii')
        print(datevar)
        mycursor.execute("INSERT INTO attendance(date,classid,slotid,courseid,stuid,attdn) VALUES(%s,%s,%s,%s,%s,\'%s\') ;"%(datevar,classid,slotid,courseid,id,"P"))
        mydb.commit()
f.close()
# except Exception:
#     print("Cool")

