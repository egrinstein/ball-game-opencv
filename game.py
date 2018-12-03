

YELLOW_MIN = (50,50,0)
YELLOW_MAX = (255,255,90)

GREEN_MIN = (0,100,0)
GREEN_MAX = (100,255,100)

RED_MIN = (0,0,100)
RED_MAX = (100,100,255)

BLACK_MIN = (0,0,0)
BLACK_MAX = (50,50,50)


COLORS = {'yellow':(YELLOW_MIN,YELLOW_MAX),
		  'green':(GREEN_MIN,GREEN_MAX)}
COLOR_NAMES = ['yellow','green']



def score(frame_to_thresh,min_values,max_values):
	(v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max) = min_values,max_values

	thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
	score = np.sum(thresh)
	return score

def detect_surrounding_color(center,frame,radius):
	left_x = max(0,center[0] - radius/2)
	right_x = min(frame.shape[0],center[0] + radius/2)
	
	left_y = max(0,center[1] - radius/2)
	right_y = min(frame.shape[1],center[1] + radius/2)

	view = frame[left_x:right_x,left_y:right_y]

	scores = {}
	for color in COLOR_NAMES:
		min_values,max_values = COLORS[color]
		scores.append(score(view,min_values,max_values))

	ind = np.argmax(scores)
	return COLOR_NAMES[ind]


class Game:
	def __init__(self):
		self.score = 0
		self.status = 1 # 1 = Playing 0 = Game over
		self.last_color = 'white' # regular tile
		self.current_position = (-1,-1)
	def update(self,frame,center,radius):
		return
		surrounding_color = detect_surrounding_color(center,frame)
		self.update_player_status(surrounding_color)

		self.message_arduino()
		
	def update_player_score(self,surrounding_color,score):
		if surrounding_color == "yellow":
			if self.last_color != yellow:
				self.score += 1
		elif surrounding_color == "green":
			self.score -= 1

	def message_arduino(self):
		# send position and score
		pass