# python dynamic_color_tracking.py --filter HSV --webcam

import cv2
import argparse
import numpy as np

from tracker import Tracker
from game import Game
from time import sleep


def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--calibrate', required=False,
                    help='Calibration mode', action='store_true')
    ap.add_argument('-n', '--nogame', required=False,
                    help='Calibration mode', action='store_true')
    args = vars(ap.parse_args())

    return args



def main():

    args = get_arguments()
    calibrate = args['calibrate']
    no_game = args['nogame']
    tracker = Tracker(calibrate=calibrate) 
    
    if not no_game:
        game = Game()

    while True:
        image, position = tracker.loop()

        if type(image) != "NoneType":
            try:
                cv2.imshow("Original", image)
            except:
                continue
        if position and not no_game:
            game.send_position_to_arduino(position)

        # Keyboard commands
        if cv2.waitKey(1) & 0xFF is ord('q'):
            game.close()
            break
        if cv2.waitKey(1) & 0xFF is ord('n'):
            game.new()

if __name__ == '__main__':
    main()