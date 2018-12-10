# python dynamic_color_tracking.py --filter HSV --webcam

import cv2
import argparse
import numpy as np

from tracker import Tracker
from game import Game



def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--calibrate', required=False,
                    help='Calibration mode', action='store_true')
    args = vars(ap.parse_args())

    return args



def main():

    args = get_arguments()
    calibrate = args['calibrate']

    tracker = Tracker(calibrate=calibrate) 
    
    if False:
        game = Game()

    while True:
        image, position = tracker.loop()

        if type(image) != "NoneType":
            cv2.imshow("Original", image)
        if position:
            if False:
                game.send_position_to_arduino(position)
            

        # Keyboard commands
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break
        if cv2.waitKey(1) & 0xFF is ord('N'):
            serial_arduino.write("N".encode())

if __name__ == '__main__':
    main()