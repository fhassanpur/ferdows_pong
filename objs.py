import pygame

# Base game object class
class FGameObject():

	def __init__(self):
		# Position and size members
		self.x = 0
		self.y = 0
		self.w = 0
		self.h = 0
		self.view = None

		# Velocity, added to position each frame
		self.vx = 0
		self.vy = 0

	def move(self):
		# Add velocity to position
		self.x = self.x + self.vx
		self.y = self.y + self.vy

	def update(self):
		self.move()

# Pong paddle class
class FPaddle(FGameObject):

	def __init__(self):
		FGameObject.__init__(self)
		self.w = 50
		self.h = 125

	def set_player_left(self):
		self.x = 50
		self.y = 250

	def set_player_right(self):
		self.x = 700
		self.y = 250

	def move_up(self):
		if self.y > 0:
			self.vy = self.vy - 1

	def move_down(self):
		if self.y < 800:
			self.vy = self.vy + 1

	def move(self):
		FGameObject.move(self)

	def check_ball_collision(self, ball):
		if ball.y >= self.y and ball.y <= self.y+self.h:
			if ball.x >= self.x and ball.x <= self.x+self.w:
				ball.reverse_direction_x()

	def render(self, surface):
		pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self.x, self.y, self.w, self.h))

	def update(self, ball):
		FGameObject.update(self)
		self.check_ball_collision(ball)

# Pong ball class
class FBall(FGameObject):

	def __init__(self):
		# Width and height used for collision detection, radius for rendering
		FGameObject.__init__(self)
		self.x = 400
		self.y = 300
		self.w = 50
		self.h = 50
		self.r = 25
		self.vx = 1
		self.vy = 1

	def reverse_direction_x(self):
		self.vx = -self.vx

	def reverse_direction_y(self):
		self.vy = -self.vy

	def collide_wall(self):
		reverse_direction_y()

	def collide_paddle(self, paddle):
		calculate_direction(paddle.y)
		reverse_direction_x()

	# The ball's new direction is based off where the ball lands on the paddle
	# If the ball lands directly in the center of the paddle, it moves horizontally
	# If the ball lands on the edge, it bounces 75 degrees perpidicular to the paddle
	def calculate_direction(self, paddle_pos_y):
		pass

	def render(self, surface):
		pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.r)

	def move(self):
		FGameObject.move(self)
		if self.x <= 0:
			pygame.event.post(pygame.event.Event(pygame.USEREVENT+2))
			self.reverse_direction_x()
		elif self.x >= 800:
			pygame.event.post(pygame.event.Event(pygame.USEREVENT+1))
			self.reverse_direction_x()
		if self.y <= 0 or self.y >= 600:
			self.reverse_direction_y()