import sys, pygame
from objs import FPaddle, FBall

class Game():
	# USEREVENT+1 is left player score
	# USEREVENT+2 is right player score

	def __init__(self):
		pass

	def start(self):
		pygame.init()
		pygame.font.init()
		width = 800
		height = 600

		self.clock = pygame.time.Clock()
		self.running = True

		self.screen = pygame.display.set_mode((width, height))

		# Creates objects
		self.ball = FBall()
		self.paddle_left = FPaddle()
		self.paddle_left.set_player_left()
		self.paddle_right = FPaddle()
		self.paddle_right.set_player_right()

		# Creates labels
		self.font = pygame.font.SysFont('Arial', 40)
		self.left_scr = 0
		self.right_scr = 0

		self.update()

	def render(self):
		self.screen.fill((0, 0, 0))
		self.render_objs()
		self.render_labels()
		pygame.display.flip()

	def ball_reset_pos(self):
		self.ball.x = 400
		self.ball.y = 300

	def left_score(self):
		self.left_scr += 1
		self.ball_reset_pos()

	def right_score(self):
		self.right_scr += 1
		self.ball_reset_pos()

	def render_labels(self):
		self.left_scr_label = self.font.render(str(self.left_scr), 0, (255, 255, 255))
		self.right_scr_label = self.font.render(str(self.right_scr), 0, (255, 255, 255))
		self.screen.blit(self.left_scr_label, (0+self.left_scr_label.get_width()*2, 50))
		self.screen.blit(self.right_scr_label, (800-self.right_scr_label.get_width()*3, 50))

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
				if event.type == pygame.QUIT: sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						self.paddle_left.move_up()
					elif event.key == pygame.K_s:
						self.paddle_left.move_down()
				if event.type == pygame.KEYUP:
					self.paddle_left.vy = 0
				if event.type == pygame.USEREVENT+1:
					self.left_score()
				if event.type == pygame.USEREVENT+2:
					self.right_score()
			self.update_objs()
			self.render()