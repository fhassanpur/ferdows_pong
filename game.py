import sys, pygame
from objs import FPaddle, FBall

class Game():
	# USEREVENT+1 is left player score
	# USEREVENT+2 is right player score
	COLOR_WHITE = (255, 255, 255)
	COLOR_BLUE = (150, 200, 255)

	def __init__(self):
		self.start()

	def start(self):
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()

		# Window Resolution
		width = 800
		height = 600

		self.running = True

		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('FerdowsPong')

		# Creates objects
		self.ball = FBall()
		self.paddle_left = FPaddle()
		self.paddle_left.set_player_left()
		self.paddle_right = FPaddle()
		self.paddle_right.set_player_right()

		# Hold is which paddle is aiming
		self.left_hold = True
		self.right_hold = False

		self.paddle_left.hold = True

		self.ball_reset_pos_left()

		# Creates labels
		self.font = pygame.font.SysFont('Arial', 40)
		self.title_label = self.font.render('FerdowsPong', 1, Game.COLOR_BLUE)
		self.left_scr = 0
		self.right_scr = 0

		# Create sound
		beep = pygame.mixer.Sound('res/beep.wav')
		boop = pygame.mixer.Sound('res/boop.wav')
		FBall.SOUND_PADDLE_HIT_0 = beep
		FBall.SOUND_PADDLE_HIT_1 = boop
		self.goal_sound = pygame.mixer.Sound('res/goal.wav')

		self.update()

	def render(self):
		self.screen.fill((0, 0, 0))
		self.render_objs()
		self.render_labels()
		pygame.display.flip()

	def ball_reset_pos_left(self):
		self.ball.x = 115
		self.ball.y = 300
		self.ball.vx = 0
		self.ball.vy = 0

	def ball_reset_pos_right(self):
		self.ball.x = 670
		self.ball.y = 300
		self.ball.vx = 0
		self.ball.vy = 0

	def left_score(self):
		self.goal_sound.play()
		self.left_scr += 1
		self.ball_reset_pos_left()
		self.paddle_left.hold = True
		self.left_hold = True

	def right_score(self):
		self.goal_sound.play()
		self.right_scr += 1
		self.ball_reset_pos_right()
		self.paddle_right.hold = True
		self.right_hold = True

	def serve_ball(self):
		if self.left_hold:
			self.ball.vx = 1
			self.paddle_left.hold = False
			self.left_hold = False
		elif self.right_hold:
			self.ball.vx = -1
			self.paddle_right.hold = False
			self.right_hold = False

	def render_labels(self):
		self.left_scr_label = self.font.render(str(self.left_scr), 0, Game.COLOR_BLUE)
		self.right_scr_label = self.font.render(str(self.right_scr), 0, Game.COLOR_BLUE)
		self.screen.blit(self.left_scr_label, (0+self.left_scr_label.get_width()*2, 50))
		self.screen.blit(self.right_scr_label, (800-self.right_scr_label.get_width()*3, 50))
		self.screen.blit(self.title_label, (400-self.title_label.get_width()/2, 50))

	def render_objs(self):
		self.ball.render(self.screen)
		self.paddle_left.render(self.screen)
		self.paddle_right.render(self.screen)

	def update_objs(self):
		self.ball.update()
		self.paddle_left.update(self.ball)
		self.paddle_right.update(self.ball)

	def update(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						self.paddle_left.move_up()
					elif event.key == pygame.K_s:
						self.paddle_left.move_down()

					if event.key == pygame.K_i:
						self.paddle_right.move_up()
					elif event.key == pygame.K_k:
						self.paddle_right.move_down()
					if event.key == pygame.K_SPACE:
						self.serve_ball()
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_w or event.key == pygame.K_s:
						self.paddle_left.vy = 0
					if event.key == pygame.K_i or event.key == pygame.K_k:
						self.paddle_right.vy = 0
				if event.type == pygame.USEREVENT+1:
					self.left_score()
				if event.type == pygame.USEREVENT+2:
					self.right_score()
			self.update_objs()
			self.render()