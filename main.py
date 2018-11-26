import cv2
import numpy as np

color_boundaries = {
                        'red':([17, 15, 100], [50, 56, 200]),
                        'green':([86, 31, 4], [220, 88, 50]),
                        'blue':([25, 146, 190], [62, 174, 250]),
                        'grey':([103, 86, 65], [145, 133, 128]),
                        'pink':([60,0,130],[255,100,255])
                    }
N_FILTER = 16 # patchsize is 40x40   

def find_max_patch(gridboard,custom_filter):
    # independent patches
    filter_size = custom_filter.shape[0]
    n = int(np.floor(gridboard.shape[0]/filter_size))
    m = int(np.floor(gridboard.shape[1]/filter_size))

    max_patch = (0,0)
    max_piecewise_mult = 0

    for i in range(n):
        for j in range(m):
            grid_patch = gridboard[i*filter_size:(i+1)*filter_size,
                                   j*filter_size:(j+1)*filter_size]
            mult = grid_patch*custom_filter

            piecewise_mult = np.sum(mult)
            if piecewise_mult > max_piecewise_mult:
                max_patch = (i,j)
                max_piecewise_mult = piecewise_mult
            
        break
    return max_patch

def get_ball_position(gridboard):
    max_patch = find_max_patch(gridboard,np.ones((N_FILTER,N_FILTER)))
    return max_patch


def render_screen(frame,ball_position):
    x,y = ball_position
    cv2.rectangle(frame,(x,y),(x+N_FILTER,y+N_FILTER),(0,0,255),thickness=5)
    cv2.imshow('frame',frame)

def preprocess_image(image):
    lower_grey,upper_grey = color_boundaries['pink']
    lower_grey = np.array(lower_grey)
    upper_grey = np.array(upper_grey)
    binary_grid = cv2.inRange(image, lower_grey, upper_grey)
    return binary_grid
    #cvtColor(image, frame_HSV, cv2.COLOR_BGR2HSV);
def game_loop(gridboard):    
    gridboard = preprocess_image(gridboard)   
    ball_position = get_ball_position(gridboard)
    render_screen(gridboard,ball_position)
             
    

def main():

    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()

    while(True):        
        ret, frame = cap.read()
        game_loop(frame)   
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break    


    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
