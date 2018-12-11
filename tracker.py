import cv2
import numpy as np

BLACK_MIN = (0,0,0)
BLACK_MAX = (50,50,50)
N_TILES = 7
BOARD_P1,BOARD_P2 = np.array((90,20)),np.array((530,460))
TILE_SIZE = (BOARD_P2[0] - BOARD_P1[0])//N_TILES

def reflect7(position):
    p0 = (4 - position[0])*2 + position[0] 
    p1 = (4 - position[1])*2 + position[1]
    return (p0,p1)

def callback(value):
    pass

def setup_trackbars():
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in "RGB":
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)


def get_trackbar_values():
    values = []

    for i in ["MIN", "MAX"]:
        for j in "RGB":
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)
    return values


class Tracker():
    def __init__(self,calibrate=False):
        self.camera = cv2.VideoCapture(1)
        self.calibrate = calibrate
        if calibrate:
            setup_trackbars()
        else:
            self.black_min,self.black_max = BLACK_MIN,BLACK_MAX

    def loop(self):
        ret, image = self.camera.read()
        if not ret:
            return None,None

        if self.calibrate:
            values = get_trackbar_values()
            self.black_min,self.black_max = values[0:3],values[3:6]
        frame_to_thresh = image.copy() # [90:530,20:460]
        
        
        thresh = cv2.inRange(frame_to_thresh, np.array(self.black_min), np.array(self.black_max))

        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
 
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
            pixel_location = None
            grid_location = None
            for i in range(N_TILES):
                for j in range(N_TILES):
                    p1 = (BOARD_P1[0] + i*TILE_SIZE,BOARD_P1[1] + j*TILE_SIZE)
                    p2 = (BOARD_P1[0] + (i+1)*TILE_SIZE,BOARD_P1[1] + (j+1)*TILE_SIZE)

                    if center[0] >= p1[0] and center[0] <= p2[0] \
                        and center[1] >= p1[1] and center[1] <= p2[1]:
                            pixel_location = tuple(p1),tuple(p2)
                            grid_location = (i+1,j+1)
                    else:
                        cv2.rectangle(image,tuple(p1),
                                        tuple(p2),(255,0,0),3)
            if grid_location:
                x_text = pixel_location[0][0]//1 + 5 #TILE_SIZE 
                y_text = pixel_location[0][1]//1 + TILE_SIZE//2 + 10
                grid_location = reflect7(grid_location)
                cv2.rectangle(image,pixel_location[0],pixel_location[1],(0,255,0),3)
                cv2.putText(image,"%d,%d" %grid_location, (x_text,y_text), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255),2)
                
                text_to_send = "%d%d" %grid_location
                
                return image,grid_location
            else:
                return image,None
        else:
            return None,None
            