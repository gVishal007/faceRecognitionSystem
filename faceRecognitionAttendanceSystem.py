import face_recognition as fr
import pyttsx3 as p
import cv2
import os
import mysql.connector as sql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

GUI = tk.Tk();
GUI.minsize(1200,1000)
GUI.title("Face Recognition Attendance System")
# All Functions start
def add_student_record(roll_no,sname,course):
 img = str(roll_no)
 roll = int(roll_no)
 conn = sql.connect(host="localhost",user="root",passwd="Vishal@2702",database="project")
 cur = conn.cursor()
 query = """insert into student_record(name,course,roll_no,image) values(%s,%s,%s,%s)"""
 cur.execute(query,(sname,course,roll,img+".jpg"))
 conn.commit()
 conn.close()
 cam = cv2.VideoCapture(0)
 cv2.namedWindow("webcam - Add Student Face")
 while True:
  ret, frame = cam.read()
  if not ret:
   print("failed to grab frame")
   break
  cv2.imshow("webcam - Add Student Face", frame)
  k = cv2.waitKey(1)
  if k%256 == 32: # SPACE pressed 
   cv2.imwrite(os.path.join('/home/vishal/Desktop/sem3_project/known_pic',img+".jpg"), frame)
   print("saved")
   break
 cam.release()
 cv2.destroyAllWindows()

def compare(sub_code):
 engine = p.init()
 cam = cv2.VideoCapture(0)
 cv2.namedWindow("webcam - take attendance")
 while True:
  ret, frame = cam.read()
  if not ret:
   print("failed to grab frame")
   break
  cv2.imshow("webcam - take attendance", frame)
  k = cv2.waitKey(1)
  if k%256 == 32:# SPACE pressed
   cv2.imwrite(os.path.join('/home/vishal/Desktop/sem3_project/temporary_pic',"random.jpg"), frame)
   print("saved")
   break
 cam.release()
 cv2.destroyAllWindows()
 conn = sql.connect(host="localhost",user="root",passwd="Vishal@2702",database="project")
 cur = conn.cursor()
 cur.execute("select image from student_record")
 result = cur.fetchall()
 result1 = "not recognize"
 for i in result :
  image1 = fr.load_image_file("known_pic/"+i[0])
  print(i[0])
  image2 = fr.load_image_file("temporary_pic/random.jpg")
  mypic_encode = fr.face_encodings(image1)[0]
  fbpic_encode = fr.face_encodings(image2)[0]
  result = fr.compare_faces([mypic_encode],fbpic_encode,tolerance=0.34)
  print(result)
  if result[0] == True:
   result1 = "recognize"
   str1 = int(i[0][0:10:1])
   cur.execute("insert into attendance(roll_no,present,subject_code) values(%s,%s,%s)",(str1,1,sub_code))
   conn.commit()
   break
 engine.setProperty('rate',120)
 engine.setProperty('voice','hindi+f3')
 engine.say("hello sir , Student "+result1+" and your attendace have beenrecorded.")
 engine.runAndWait()
def add_student_face():
 new1 = tk.Toplevel(GUI)
 new1.title("Face Recognition Attendace System")
 new1.minsize(1200,650)
 bg2 = tk.PhotoImage(file="face2.png")
 tk.Label(new1,image=bg2).place(x=50,y=50)
 s1 = tk.Label(new1,text="Student Name",font="Times 18")
 s1.place(x=700,y=100)
 sname = tk.Entry(new1,textvariable=tk.StringVar())
 sname.place(x=900,y=100)
 s1 = tk.Label(new1,text="Student Roll Number \n (ex2019104074)",font="Times 18")
 s1.place(x=650,y=150)
 sroll = tk.Entry(new1,textvariable=tk.StringVar())
 sroll.place(x=900,y=150)
 tk.Label(new1,text="Select your course",font="Times18").place(x=650,y=220)
 course = ttk.Combobox(new1,width=25,textvariable=tk.StringVar())
 course['values'] = ('MCA','B-tech','M-tech','MBA')
 course.place(x=900,y=220)
 def upload():
  sn = sname.get()
  roll = sroll.get()
  s_course = course.get()
  add_student_record(roll,sn,s_course)
  messagebox.showinfo('Face Capturing','Your Data Uploaded Successfully')
  sname.delete(0,'end')
  sroll.delete(0,'end')
  tk.Button(new1,text="Upload Data",command=upload).place(x=900,y=350)
 new1.mainloop()
def get_subject_code():
 new3 = tk.Toplevel(GUI)
 new3.title("Face Recognition Attendance System")
 new3.minsize(1000,650)
 tk.Label(new3,text="Welcome to Face Recognition Attendance System",font="Times 32").place(x=50,y=20)
 bg = tk.PhotoImage(file="mmmut.png")
 tk.Label(new3,image=bg).place(x=350,y=100)
 tk.Label(new3,text="Enter Subject Code",font="Times 18").place(x=250,y=350)
 subject_code = tk.Entry(new3,textvariable=tk.StringVar())
 subject_code.place(x=450,y=350)
 def scan():
  compare(subject_code.get())
  messagebox.showinfo('Attendace System','Your Attendace recorded successfully')
 tk.Button(new3,text="Take attendance",command=scan).place(x=380,y=400)
 new3.mainloop()
def get_list():
 new4 = tk.Toplevel(GUI)
 new4.title("Face Recognition Attendance System")
 new4.minsize(800,650)
 bg = tk.PhotoImage(file="student1.png")
 tk.Label(new4,image=bg).place(x=50,y=50)
 tk.Label(new4,text="Student Roll Number \n (ex2019104074)",font="Times 18").place(x=400,y=50)
 r_number = tk.Entry(new4,textvariable=tk.StringVar())
 r_number.place(x=430,y=150)
 def get_student_list():
  number = r_number.get()
  conn = sql.connect(host="localhost",user="root",passwd="Vishal@2702",database="project")
  cur = conn.cursor()
  query = "select roll_no,subject_code,attendance_date from attendance where roll_no ='"+number+"'"
  cur.execute(query)
  result = cur.fetchall()
  print(result)
  conn.commit()
  conn.close()
  new5 = tk.Toplevel(GUI)
  new5.title("Face Recognition Attendance System")
  new5.minsize(800,750)
  tk.Label(new5,text="Roll Number________Subject code____________Date(YYYY-MM-DD)",font="Times18").place(x=1,y=10)
  y1=50
  for i in result:
   x1=1
   for j in i :
    tk.Label(new5,text=j,font="Times 18").place(x=x1,y=y1)
    x1=x1+250
    y1=y1+50
  new5.mainloop()
 tk.Button(new4,text="Get attendance",command=get_student_list).place(x=455,y=200)
 new4.mainloop()
def submit():
 uname = entry1.get()
 upass = entry2.get()
 if uname == "vishal" and upass == "gupta":
  messagebox.showinfo('Login','login successful')
  new = tk.Toplevel(GUI)
  new.title("Face Recognition Attendace System")
  new.minsize(800,650)
  bg2 = tk.PhotoImage(file="mmmut.png")
  tk.Label(new,image=bg2).place(x=300,y=50)
  b1 = tk.Button(new,text="Add New Student Image",command=add_student_face)
  b1.place(x=100,y=300)
  b2 = tk.Button(new,text="Take Attendance",command=get_subject_code)
  b2.place(x=100,y=350)
  b2 = tk.Button(new,text="Attendance list",command=get_list)
  b2.place(x=100,y=400)
  new.mainloop()
 else:
  messagebox.showinfo('Login','Wrong credential')
  # All Functions end
tk.Label(GUI,text="Madan Mohan Malaviya University of Technology,Gorakhpur",font="Times 30").place(x=80,y=50)
tk.Label(GUI,text="Welcome to Face Recognition Attendace Management System",font="Times 26").place(x=150,y=100)
tk.Label(GUI,text="by Vishal Gupta \nMCA\n 2019104074",font="Times18").place(x=950,y=920)
bg = tk.PhotoImage(file="face5.png")
tk.Label(GUI,image=bg).place(x=350,y=150)
bg1 = tk.PhotoImage(file="login.png")
tk.Label(GUI,image=bg1).place(x=150,y=550)
l1 = tk.Label(GUI,text="User Name",font=('Times',18))
l1.place(x=450,y=650) # set label in place x=250 and y=380
# create entry for user name
entry1 = tk.Entry(GUI,textvariable=tk.StringVar())
entry1.place(x=670,y=650) # set entry in place x=370 and y=380
# create label for password
l2 = tk.Label(GUI,text="Password",font=('Times',18))
l2.place(x=450,y=700) # set label in place x=250 and y=420
# create entry for password which show *
entry2 = tk.Entry(GUI,textvariable=tk.StringVar(),show='*')
entry2.place(x=670,y=700) # set entry in place x=370 and y=420
# create submit button
b1 = tk.Button(GUI,text="Submit",command=submit)
b1.place(x=600,y=750) # set button in place x=400 and y=450

GUI.mainloop()
