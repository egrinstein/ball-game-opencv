# python dynamic_color_tracking.py --filter HSV --webcam

import cv2
import argparse
import numpy as np
import serial


N_TILES = 7
BOARD_P1,BOARD_P2 = np.array((90,20)),np.array((530,460))
TILE_SIZE = (BOARD_P2[0] - BOARD_P1[0])//N_TILES

BLACK_MIN = (0,0,0)
BLACK_MAX = (50,50,50)

def callback(value):
    pass


def setup_trackbars(range_filter):
    cv2.namedWindow("Trackbars", 0)

    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filter', required=True,
                    help='Range filter. RGB or HSV')
    ap.add_argument('-w', '--webcam', required=False,
                    help='Use webcam', action='store_true')
    ap.add_argument('-c', '--calibrate', required=False,
                    help='Calibration mode', action='store_true')
    args = vars(ap.parse_args())

    if not args['filter'].upper() in ['RGB', 'HSV']:
        ap.error("Please speciy a correct filter.")

    return args


def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)
    return values

def get_ball_values():
    return BLACK_MIN + BLACK_MAX

def main():

    ser = serial.Serial('COM3', 9600, timeout=0)
    args = get_arguments()
    camera = cv2.VideoCapture(1)


    range_filter = args['filter'].upper()
    calibrate = args['calibrate']


    if calibrate:
        setup_trackbars(range_filter)


    # Main loop

    while True:
        ret, image = camera.read()
        if not ret:
            break
        
       
        if calibrate:
            v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)
        else:
            v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_ball_values()

        frame_to_thresh = np.transpose(image.copy()[90:530,20:460])
        
        thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))

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
 
            absolute_location = None
            discrete_location = None
            for i in range(N_TILES):
                for j in range(N_TILES):
                    p1 = (BOARD_P1[0] + i*TILE_SIZE,BOARD_P1[1] + j*TILE_SIZE)
                    p2 = (BOARD_P1[0] + (i+1)*TILE_SIZE,BOARD_P1[1] + (j+1)*TILE_SIZE)

                    if center[0] >= p1[0] and center[0] <= p2[0] \
                        and center[1] >= p1[1] and center[1] <= p2[1]:
                            absolute_location = tuple(p1),tuple(p2)
                            discrete_location = (i+1,j+1)
                    else:
                        cv2.rectangle(image,tuple(p1),
                                        tuple(p2),(255,0,0),3)
            if absolute_location:
                x_text = absolute_location[0][0]//1 + 5 #TILE_SIZE 
                y_text = absolute_location[0][1]//1 + TILE_SIZE//2 + 10
                cv2.rectangle(image,absolute_location[0],absolute_location[1],(0,255,0),3)
                cv2.putText(image,"%d,%d" %discrete_location, (x_text,y_text), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 0, 255),2)
                
                text_to_send = "%d%d" %discrete_location
                ser.write(var)
                    
        # show the frame to our screen
        cv2.imshow("Original", image)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF is ord('q'):
            break
        if cv2.waitKey(1) & 0xFF is ord('N'):
            ser.write("N")

if __name__ == '__main__':
    main()