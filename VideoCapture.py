import cv2

class MyVideoCapture:
    imageRotate = 0
    imageSkale = 1.0
    imageMirror = True
    radius = 40
    color = (0, 0, 255) # Red color in BGR
    thickness = 1      # Line thickness of 5 px
    enabelCircle = False
    enabelCross = False
    diagonalCross = False

    def __init__(self, video_source=0):
         # Open the video source

        # self.cv2.namedWindow("preview ")
        self.vc = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        if not self.vc.isOpened():
            raise ValueError("Unable to open video source", video_source)
 
        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)

        # Get video source width and height
        self.width = int(self.vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.cX = int(self.width // 2)
        self.cY = int(self.height // 2)

    def get_frame(self):
        if self.vc.isOpened(): # try to get the first frame
            rval, frame = self.vc.read()
            if rval:
                if self.imageMirror: frame = cv2.flip(frame,1)           #spiegeln

                # rotate our image by 45 degrees around the center of the image
                M = cv2.getRotationMatrix2D((self.cX, self.cY), self.imageRotate, self.imageSkale)
                frame = cv2.warpAffine(frame, M, (self.width, self.height))

                if self.enabelCircle: frame = cv2.circle(frame, (self.cX, self.cY), self.radius, self.color, self.thickness)     #Kreis
                if self.enabelCross:
                    if self.diagonalCross:
                        x1 = [(0,0),(self.width,self.height)]
                        x2 = [(0,self.height),(self.width,0)]
                    else:
                        x1 = [(0,self.cY),(self.width,self.cY)]
                        x2 = [(self.cX,0),(self.cX, self.height)]
                    frame = cv2.line(frame, x1[0],x1[1], self.color, self.thickness)            #Linie 1  
                    frame = cv2.line(frame, x2[0],x2[1], self.color, self.thickness)            #Linie 2
                # Return a boolean success flag and the current frame converted to BGR
                return (rval, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (rval, None)
        else:
            return (rval, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vc.isOpened():
            self.vc.release()