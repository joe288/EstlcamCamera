import tkinter
from tkinter import *
import VideoCapture
import cv2
import PIL.Image, PIL.ImageTk
import time

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

        self.cb_imageMirrorState = IntVar()
        self.cb_imageMirrorState.set(1)
        self.cb_imageMirror=tkinter.Checkbutton(imageFrame, text="mirror", variable=self.cb_imageMirrorState ,command=self.mirror)
        self.cb_imageMirror.pack(anchor=W) 

        self.lb_rotate = Label(imageFrame, text="Rotate:")
        self.lb_rotate.pack(anchor=W)
        rotate_value = tkinter.StringVar(value=self.vid.imageRotate)
        self.sb_rotate = tkinter.Spinbox(imageFrame, width=5, from_=0, to=360, textvariable = rotate_value ,command=self.setRotate)
        self.sb_rotate.pack(anchor=W) 

        self.lb_skale = Label(imageFrame, text="Skale:")
        self.lb_skale.pack(anchor=W)
        skale_value = tkinter.StringVar(value=self.vid.imageSkale)
        self.sb_skale = tkinter.Spinbox(imageFrame, from_=1.0, to=5.0, width=5, increment=0.1, textvariable = skale_value ,command=self.setSkale)
        self.sb_skale.pack(anchor=W) 

        circleFrame = LabelFrame(settingsFrame, text="Circle")
        circleFrame.pack(fill="both", expand="yes")

        self.cb_circleState = IntVar()
        self.cb_circle=tkinter.Checkbutton(circleFrame, text="enbale", variable=self.cb_circleState ,command=self.circle)
        self.cb_circle.pack(anchor=W) 

        self.lb_circle = Label(circleFrame, text="Size:")
        self.lb_circle.pack(anchor=W)
        circle_value = tkinter.StringVar(value=self.vid.radius)
        self.sb_circle = tkinter.Spinbox(circleFrame, from_=10, to=100, width=5, textvariable = circle_value ,command=self.setCircleDia)
        self.sb_circle.config(state='disabled')
        self.sb_circle.pack(anchor=W) 

        crossFrame = LabelFrame(settingsFrame, text="Cross")
        crossFrame.pack(fill="both", expand="yes")

        self.cb_crossState = IntVar()
        self.cb_cross=tkinter.Checkbutton(crossFrame, text="enbale", variable=self.cb_crossState ,command=self.cross)
        self.cb_cross.pack(anchor=W) 

        self.cb_crossDiagonalState = IntVar()
        self.cb_crossDiagonal=tkinter.Checkbutton(crossFrame, text="diagonal", variable=self.cb_crossDiagonalState ,command=self.crossDiagonal)
        self.cb_crossDiagonal.config(state='disabled')
        self.cb_crossDiagonal.pack(anchor=W) 

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(settingsFrame, text="Snapshot", width=20, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=False)

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
        self.vid.imageRotate = int(self.sb_rotate.get())

    def setSkale(self):
        self.vid.imageSkale = float(self.sb_skale.get())

    def setCircleDia(self):
        self.vid.radius= int(self.sb_circle.get())

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

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")