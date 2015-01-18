import sys, pygame

class Game():


	def __init__(self):
		pass

	def start(self):
		pygame.init()
		width = 800
		height = 600

		self.screen = pygame.display.set_mode(width, height)