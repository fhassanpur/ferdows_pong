# Created by Ferdows Hassanpur
# www.ferdows.me

import pygame

# Base game object class
class FGameObject():
	COLOR_WHITE = (255, 255, 255)

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
		self.x += self.vx
		self.y += self.vy

	def update(self):
		self.move()

# Pong paddle class
class FPaddle(FGameObject):

	def __init__(self):
		FGameObject.__init__(self)
		self.w = 30
		self.h = 125
		self.hold = False

	def set_player_left(self):
		self.x = 50
		self.y = 250

	def set_player_right(self):
		self.x = 700
		self.y = 250

	def move_up(self):
		if self.y >= 0:
			self.vy -= 1

	def move_down(self):
		if self.y <= 800:
			self.vy += 1

	def aim_ball(self, ball):
		ball.y = self.y+self.h/2

	def move(self):
		FGameObject.move(self)

	def check_ball_collision(self, ball):
		if ball.y >= self.y and ball.y <= self.y+self.h:
			if ball.x >= self.x and ball.x <= self.x+self.w:
				ball.collide_paddle(self)

	def render(self, surface):
		pygame.draw.rect(surface, FGameObject.COLOR_WHITE, pygame.Rect(self.x, self.y, self.w, self.h))

	def update(self, ball):
		FGameObject.update(self)
		if not self.hold:
			self.check_ball_collision(ball)
		else:
			self.aim_ball(ball)

# Pong ball class
class FBall(FGameObject):
	SOUND_PADDLE_HIT_0 = None
	SOUND_PADDLE_HIT_1 = None
	SOUND_CHOICE = 0

	def __init__(self):
		# Width and height used for collision detection, radius for rendering
		FGameObject.__init__(self)
		self.x = 400
		self.y = 300
		self.w = 50
		self.h = 50
		self.r = 20
		self.vx = 1
		self.vy = 1

		# Pall is paused after goal, left or right paddle aims on hold
		self.left_hold = False
		self.right_hold = False

	def reverse_direction_x(self):
		self.vx = -self.vx

	def reverse_direction_y(self):
		self.vy = -self.vy

	def collide_wall(self):
		self.reverse_direction_y()

	def collide_paddle(self, paddle):
		if FBall.SOUND_CHOICE == 0:
			FBall.SOUND_PADDLE_HIT_0.play()
			FBall.SOUND_CHOICE = 1
		elif FBall.SOUND_CHOICE == 1:
			FBall.SOUND_PADDLE_HIT_1.play()
			FBall.SOUND_CHOICE = 0
		self.reverse_direction_x()
		self.calculate_direction(paddle)

	# The ball's new direction is based off where the ball lands on the paddle
	# If the ball lands directly in the center of the paddle, it moves horizontally
	# If the ball lands on the edge, it bounces by 2 and 1 in between
	def calculate_direction(self, paddle):
		if self.y == paddle.y+paddle.h/2:
			self.vy = 0
		elif self.y < paddle.y+paddle.h/2 and self.y >= paddle.y+paddle.h/4 or self.y > paddle.y+paddle.h/2 and self.y <= paddle.y+paddle.h/2+paddle.h/4:
			if self.vy >= 0:
				self.vy = 1
			elif self.vy < 0:
				self.vy = -1
		elif self.y < paddle.y+paddle.h/4 and self.y >= paddle.y or self.y > paddle.y+paddle.h/2+paddle.h/4 and self.y <= paddle.y+paddle.h:
			if self.vy >= 0:
				self.vy = 2
			elif self.vy < 0:
				self.vy = -2


	def render(self, surface):
		pygame.draw.circle(surface, FGameObject.COLOR_WHITE, (self.x, self.y), self.r)

	def move(self):
		FGameObject.move(self)
		if self.x <= 0:
			pygame.event.post(pygame.event.Event(pygame.USEREVENT+2))
		elif self.x >= 800:
			pygame.event.post(pygame.event.Event(pygame.USEREVENT+1))
		if self.y <= 0 or self.y >= 600:
			self.collide_wall()