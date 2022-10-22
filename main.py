from macpath import join
from random import random
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
from turtle import width
import cv2,os
import csv
import numpy
from PIL import Image
import pandas
import datetime

#=====================================================================================

    
def openperformance():
    newWindow = Toplevel(window)
    newWindow.title("Performance Window")
    newWindow.resizable(True,False)
    newWindow.geometry("1280x720")
    Label(newWindow, text="Health Performance page").pack()

    
    frameper = tkinter.Frame(newWindow, bg="gray")
    frameper.place(x=35,y=60, relwidth=0.95, relheight=0.80)

        
    tv= ttk.Treeview(frameper,height=20,columns = ('name','date','time','absent','reason'))
    tv.column('#0',width=82)
    tv.column('name',width=130)
    tv.column('date',width=133)
    tv.column('time',width=133)
    tv.column('absent',width=133)
    tv.column('reason',width=133)

    tv.grid(row=2,column=0,padx=(240,0),pady=(0,0),columnspan=6)
    tv.heading('#0',text ='ID')
    tv.heading('name',text ='NAME')
    tv.heading('date',text ='DATE')
    tv.heading('time',text ='TIME')
    tv.heading('absent',text ='ABSENT')
    tv.heading('reason',text ='REASON')


    

    performance = tkinter.Button(frameper, text="Performance = "
    ,fg="white"  ,bg="black"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
    performance.place(x=400, y=480)


    performance.configure(text='Performance =  '+ str(71) + '%')

    rollText = tkinter.Label(frameper, text="Enter your Employee ID",width=18  ,fg="white"  ,bg="orange" ,font=('times', 14, ' bold ') )
    rollText.place(x=5, y=10)
    rollEdit = tkinter.Entry(frameper,width=18 ,fg="black",font=('times', 15, ' bold '))
    rollEdit.place(x=5, y=40)


    #Fetching ID

    # with open('EmployeeDetails\EmployeeDetails.csv', 'r') as csvFile1:
    #     reader1 = csv.reader(csvFile1)
    #     rows = list(reader1)
    #     print (rows[2][2])

    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 2
            if (i > 1):
                iidd = str(lines[0]) + '   '
                tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
           
   

       

       
        csvFile1.close()

    

    


    

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#=====================================================================================

def tick():
    time_string = datetime.datetime.now().strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

#=====================================================================================

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        messagebox._show(title='File missing', message='haarcascade file is missing')
        window.destroy()

#=========================================================================================

def clear():
    rollEdit.delete(0, 'end')
    

def clear1():
    nameEdit.delete(0, 'end')
   

#=========================================================================================

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("EmployeeDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
    if exists:
       for row in open("EmployeeDetails\EmployeeDetails.csv"):
            serial = serial + 1
    else:
        with open("EmployeeDetails\EmployeeDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()

    Id = (rollEdit.get())
    name = (nameEdit.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 4)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 110:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('EmployeeDetails\EmployeeDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
     
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

#=========================================================================================

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
  
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, numpy.array(ID))
    except:
        messagebox._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
  
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))

#=========================================================================================

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = numpy.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

#=========================================================================================

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("EmployeeDetails/")
    for k in tv.get_children():
        tv.delete(k)
   
    i = 0
  
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        messagebox._show(title='Data Missing', message='Please click on Save Profile to save data')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
    if exists1:
        df = pandas.read_csv("EmployeeDetails\EmployeeDetails.csv")
    else:
        messagebox._show(title='Details Missing', message='Employee details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.05, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                
                date = datetime.datetime.now().strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.now().strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
  
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

#=========================================================================================
ts = datetime.datetime.now()
date = ts.strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

#================================= GUI ===================================

window = tkinter.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#8f4155')

frame1 = tkinter.Frame(window, bg="gray")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)
frame2 = tkinter.Frame(window, bg="pink")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)
title = tkinter.Label(window, text="Facial Recognition Attendance System" ,
fg="white",bg="#262523" ,width=58 ,height=1,font=('Comic Sans Ms', 29, ' bold '))
title.place(x=9, y=10)

#DATE GUI
dateBox = tkinter.Frame(window, bg="")
dateBox.place(x=10, y=71, relwidth=0.16, relheight=0.06)
datef = tkinter.Label(dateBox, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="white",bg="#8f4155" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

#TIME GUI
timeBox= tkinter.Frame(window, bg="orange")
timeBox.place(x=220, y=73, relwidth=0.09, relheight=0.06)
clock = tkinter.Label(timeBox,fg="orange",bg="#8f4155" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

head2 = tkinter.Label(frame2, text="                       For New Registrations                       ",
fg="black",bg="#E389B9" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)
head1 = tkinter.Label(frame1, text="                       For Already Registered                       ",
fg="black",bg="#746AB0" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

# ENTRY FIELDS
rollText = tkinter.Label(frame2, text="Enter your Employee No",width=30  ,fg="white"  ,bg="#FFCE30" ,font=('times', 18, ' bold ') )
rollText.place(x=0, y=90)
rollEdit = tkinter.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
rollEdit.place(x=60, y=130)

nameText = tkinter.Label(frame2, text="Enter Name",width=30  ,fg="white"  ,bg="#FFCE30" ,font=('times', 18, ' bold '))
nameText.place(x=0, y=190)
nameEdit = tkinter.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
nameEdit.place(x=60, y=230)

message = tkinter.Label(frame2, text="" ,bg="pink" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=9, y=480)

attendanceText = tkinter.Label(frame1, text="Attendance Sheet"  ,fg="white"  ,bg="gray"  ,height=1 ,font=('times', 17, ' bold '))
attendanceText.place(x=140, y=50)
res=0
exists = os.path.isfile("EmployeeDetails\EmployeeDetails.csv")
if exists:
    for row in open("EmployeeDetails\EmployeeDetails.csv"):
        res = res + 1
    res = res - 4
else:
    res = 0
    
message.configure(text='Total Employee Registrations till now  : '+str(res))

#================================= TREE VIEW TABLE ===================================

tv= ttk.Treeview(frame1,height=12,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(90,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

#================================= SCROLL BAR ===================================

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,0),pady=(90,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

#================================= BUTTONS ===================================

clearButton = tkinter.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=130)
clearButton2 = tkinter.Button(frame2, text="Clear", command=clear1  ,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=230)    
takeImg = tkinter.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=320)
trainImg = tkinter.Button(frame2, text="Save Profile", command=TrainImages ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=390)

trackImg = tkinter.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="black"  ,bg="#00CDAC"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=400)
quitWindow = tkinter.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

performance = tkinter.Button(frame1, text="Employee Performance", command=openperformance
,fg="white"  ,bg="green"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
performance.place(x=30, y=506)


window.mainloop()