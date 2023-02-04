import tkinter
from tkinter import *
import VideoCapture
import cv2
import PIL.Image, PIL.ImageTk
import time
import json
import os

systemFile = "settings.json"

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = VideoCapture.MyVideoCapture(self.video_source)
        
        streamFrame = Frame(window)
        streamFrame.pack(side = LEFT )

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(streamFrame, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        settingsFrame = Frame(window)
        settingsFrame.pack(side = RIGHT )

        imageFrame = LabelFrame(settingsFrame, text="Image")
        imageFrame.pack(fill="both", expand="yes")

        self.load()

        self.cb_imageMirror=tkinter.Checkbutton(imageFrame, text="mirror", variable=self.cb_imageMirrorState ,command=self.mirror)
        self.cb_imageMirror.pack(anchor=W) 

        self.lb_rotate = Label(imageFrame, text="Rotate:")
        self.lb_rotate.pack(anchor=W)

        self.sb_rotate = tkinter.Spinbox(imageFrame, width=5, from_=0, to=360, increment=0.1, textvariable = self.rotate_value ,command=self.setRotate)
        self.sb_rotate.pack(anchor=W) 

        self.lb_skale = Label(imageFrame, text="Skale:")
        self.lb_skale.pack(anchor=W)

        self.sb_skale = tkinter.Spinbox(imageFrame, width=5, from_=1, to=5, increment=0.1, textvariable = self.skale_value ,command=self.setSkale)
        self.sb_skale.pack(anchor=W) 

        circleFrame = LabelFrame(settingsFrame, text="Circle")
        circleFrame.pack(fill="both", expand="yes")

        self.cb_circle=tkinter.Checkbutton(circleFrame, text="enbale", variable=self.cb_circleState ,command=self.circle)
        self.cb_circle.pack(anchor=W) 

        self.lb_circle = Label(circleFrame, text="Size:")
        self.lb_circle.pack(anchor=W)
     
        self.sb_circle = tkinter.Spinbox(circleFrame, from_=10, to=100, width=5, textvariable = self.circle_value ,command=self.setCircleDia)
        if not self.cb_circleState.get() == 1:
            self.sb_circle.config(state='disabled')
        self.sb_circle.pack(anchor=W) 

        crossFrame = LabelFrame(settingsFrame, text="Cross")
        crossFrame.pack(fill="both", expand="yes")

        self.cb_cross=tkinter.Checkbutton(crossFrame, text="enbale", variable=self.cb_crossState ,command=self.cross)
        self.cb_cross.pack(anchor=W) 

        self.cb_crossDiagonal=tkinter.Checkbutton(crossFrame, text="diagonal", variable=self.cb_crossDiagonalState ,command=self.crossDiagonal)
        if not self.cb_crossState.get() == 1:
            self.cb_crossDiagonal.config(state='disabled')
        self.cb_crossDiagonal.pack(anchor=W) 

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(settingsFrame, text="Snapshot", width=20, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=False)

        self.btn_save=tkinter.Button(settingsFrame, text="Save", width=20, command=self.save)
        self.btn_save.pack(anchor=tkinter.CENTER, expand=False)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        self.window.mainloop()

    def mirror(self):
        if self.cb_imageMirrorState.get():
            self.vid.imageMirror = True
        else:
            self.vid.imageMirror = False

    def setRotate(self):
        self.vid.imageRotate = float(self.rotate_value.get())

    def setSkale(self):
        self.vid.imageSkale = float(self.skale_value.get())

    def setCircleDia(self):
        self.vid.radius= int(self.circle_value.get())

    def circle(self):
        if not self.cb_circleState.get():
            self.vid.enabelCircle = False
            self.sb_circle.config(state='disabled')
        else: #
            self.vid.enabelCircle = True
            self.sb_circle.config(state='normal')
    
    def cross(self):
        if self.cb_crossState.get():
            self.vid.enabelCross = True
            self.cb_crossDiagonal.config(state='normal')
        else:
            self.vid.enabelCross = False
            self.cb_crossDiagonal.config(state='disabled')

    def crossDiagonal(self):
        if self.cb_crossDiagonalState.get():
            self.vid.diagonalCross = True
        else:
            self.vid.diagonalCross = False

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def save(self):
        dictionary = {
        "mirror": self.cb_imageMirrorState.get(),
        "rotate": self.rotate_value.get(),
        "scale": self.skale_value.get(),
        "circleDia": self.circle_value.get(),
        "circle": self.cb_circleState.get(),
        "cross": self.cb_crossState.get(),
        "crossDiagonal": self.cb_crossDiagonalState.get()
        }
 
        with open(systemFile, "w") as outfile:
            json.dump(dictionary, outfile)

    def load(self):
        self.cb_imageMirrorState = IntVar()
        self.cb_circleState = IntVar()
        self.cb_crossState = IntVar()
        self.cb_crossDiagonalState =IntVar()
        self.rotate_value = IntVar()
        self.skale_value = IntVar()
        self.circle_value = IntVar()

        # JSON file
        if os.path.isfile(systemFile): 
            f = open (systemFile, "r")
            
            # Reading from file
            data = json.loads(f.read())
            
            self.cb_imageMirrorState.set(data["mirror"])
            self.mirror()

            self.rotate_value = tkinter.StringVar(value = data["rotate"])
            self.setRotate()

            self.skale_value = tkinter.StringVar(value = data["scale"])
            self.setSkale()       
            
            self.circle_value = tkinter.StringVar(value = data["circleDia"])
            self.setCircleDia()

            self.cb_circleState.set(data["circle"])
            self.vid.enabelCircle = self.cb_circleState.get()

            self.cb_crossDiagonalState.set(data["crossDiagonal"])

            self.cb_crossState.set(data["cross"])
            self.vid.enabelCross = self.cb_crossState.get()
            self.vid.diagonalCross = self.cb_crossDiagonalState.get()
            # Closing file
            f.close()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")