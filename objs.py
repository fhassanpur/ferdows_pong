# Base game object class
class FGameObject():

	def __init__(self):
		# Position and size members
		self.x = 0
		self.y = 0
		self.w = 0
		self.h = 0

		# Velocity, reset each frame
		self.vx = 0
		self.vy = 0

	def move(self):
		# Add velocity to position
		self.x = self.x + self.vx
		self.y = self.y + self.xy

		# Reset velocity
		self.vx, self.vy = 0

	def update(self):
		self.move()

# Pong paddle class
class FPaddle(FGameObject):

	def __init__(self):
		self.w = 50
		self.h = 100

	def set_player_left(self):
		self.x = 50
		self.y = 50

	def set_player_right(self):
		self.x = 700
		self.y = 50