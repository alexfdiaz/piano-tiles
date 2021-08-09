import pygame, sys
from data.settings import Settings
from data.tile import Tile
from random import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)

RED = (255, 80, 80)
GREEN = (80, 255, 80)
BLUE = (80, 80, 255)
YELLOW = (255, 255, 80)

LIGHT_RED = (255, 220, 220)
LIGHT_GREEN = (220, 255, 220)
LIGHT_BLUE = (220, 220, 255)
LIGHT_YELLOW = (255, 255, 220)

class Game:
	def __init__(self):
		self.settings = Settings()
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))
		self.caption = pygame.display.set_caption(self.settings.CAPTION)
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(self.settings.FONT, 20)
		self.big_font = pygame.font.Font(self.settings.FONT, 26)

		self._play = False
		self._lose = False
		self.perfect_game = True

		self.tile_vel = 0


		self._bottom_rect = pygame.rect.Rect(0, self.settings.HEIGHT + 105, self.settings.WIDTH, 20)

		self._A = self.font.render('A', True, WHITE)
		self._A_rect = self._A.get_rect()
		self._A_rect.center = (50, self.settings.HEIGHT - 100)

		self._S = self.font.render('S', True, WHITE)
		self._S_rect = self._S.get_rect()
		self._S_rect.center = (150, self.settings.HEIGHT - 100)

		self._K = self.font.render('K', True, WHITE)
		self._K_rect = self._K.get_rect()
		self._K_rect.center = (250, self.settings.HEIGHT - 100)

		self._L = self.font.render('L', True, WHITE)
		self._L_rect = self._L.get_rect()
		self._L_rect.center = (350, self.settings.HEIGHT - 100)


		self._piano_tiles = self.big_font.render('Piano Tiles', True, BLACK)
		self._piano_tiles_rect = self._piano_tiles.get_rect()
		self._piano_tiles_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 - 100)

		self._select = self.font.render('Select difficulty', True, BLACK)
		self._select_rect = self._select.get_rect()
		self._select_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 - 50)

		self._easy = self.font.render('easy', True, BLACK)
		self._easy_rect = self._easy.get_rect()
		self._easy_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2)
		self._easy_button = self._easy_rect.copy()
		self._easy_button.x -= 10
		self._easy_button.y -= 10
		self._easy_button.w += 20
		self._easy_button.h += 20
		self._easy_hover = False

		self._medium = self.font.render('medium', True, BLACK)
		self._medium_rect = self._medium.get_rect()
		self._medium_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 + 50)
		self._medium_button = self._medium_rect.copy()
		self._medium_button.x -= 10
		self._medium_button.y -= 10
		self._medium_button.w += 20
		self._medium_button.h += 20
		self._medium_hover = False

		self._hard = self.font.render('hard', True, BLACK)
		self._hard_rect = self._hard.get_rect()
		self._hard_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 + 100)
		self._hard_button = self._hard_rect.copy()
		self._hard_button.x -= 10
		self._hard_button.y -= 10
		self._hard_button.w += 20
		self._hard_button.h += 20
		self._hard_hover = False

		self._playagain = self.font.render('play again', True, BLACK)
		self._playagain_rect = self._playagain.get_rect()
		self._playagain_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 + 50)
		self._playagain_button = self._playagain_rect.copy()
		self._playagain_button.x -= 10
		self._playagain_button.y -= 10
		self._playagain_button.w += 20
		self._playagain_button.h += 20
		self._playagain_hover = False

		self._quit = self.font.render('quit', True, BLACK)
		self._quit_rect = self._quit.get_rect()
		self._quit_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 + 100)
		self._quit_button = self._quit_rect.copy()
		self._quit_button.x -= 10
		self._quit_button.y -= 10
		self._quit_button.w += 20
		self._quit_button.h += 20
		self._quit_hover = False


		self.cols = [[], [], [], []]
		self.score = 0

		self._score = self.font.render(f'{self.score}', True, BLACK)
		self._score_rect = self._score.get_rect()
		self._score_rect.center = (self.settings.WIDTH // 2, 12)

		self.star = pygame.image.load('data/star.png')
		self.star_rect = self.star.get_rect()
		self.star_rect.center = (self.settings.WIDTH - 12, 12)


		self._yourscore = self.font.render('Your score', True, BLACK)
		self._yourscore_rect = self._yourscore.get_rect()
		self._yourscore_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 - 100)

	def draw(self):
		self.screen.fill(self.settings.BG_COLOR)

		pygame.draw.rect(self.screen, LIGHT_RED, (0, 0, 100, self.settings.HEIGHT))
		pygame.draw.rect(self.screen, LIGHT_YELLOW, (100, 0, 100, self.settings.HEIGHT))
		pygame.draw.rect(self.screen, LIGHT_GREEN, (200, 0, 100, self.settings.HEIGHT))
		pygame.draw.rect(self.screen, LIGHT_BLUE, (300, 0, 100, self.settings.HEIGHT))

		for col in self.cols:
			for tile in col:
				pygame.draw.rect(self.screen, tile.color, tile.rect)

		pygame.draw.line(self.screen, LIGHT_YELLOW, (100, 0), (100, self.settings.HEIGHT), 2)
		pygame.draw.line(self.screen, LIGHT_GREEN, (200, 0), (200, self.settings.HEIGHT), 2)
		pygame.draw.line(self.screen, LIGHT_BLUE, (300, 0), (300, self.settings.HEIGHT), 2)

		pygame.draw.line(self.screen, RED, (0, self.settings.HEIGHT - 100), (100, self.settings.HEIGHT - 100), 2)
		pygame.draw.line(self.screen, YELLOW, (100, self.settings.HEIGHT - 100), (200, self.settings.HEIGHT - 100), 2)
		pygame.draw.line(self.screen, GREEN, (200, self.settings.HEIGHT - 100), (300, self.settings.HEIGHT - 100), 2)
		pygame.draw.line(self.screen, BLUE, (300, self.settings.HEIGHT - 100), (400, self.settings.HEIGHT - 100), 2)

		pygame.draw.circle(self.screen, RED, (50, self.settings.HEIGHT - 100), 20)
		pygame.draw.circle(self.screen, YELLOW, (150, self.settings.HEIGHT - 100), 20)
		pygame.draw.circle(self.screen, GREEN, (250, self.settings.HEIGHT - 100), 20)
		pygame.draw.circle(self.screen, BLUE, (350, self.settings.HEIGHT - 100), 20)

		self.screen.blit(self._A, self._A_rect)
		self.screen.blit(self._S, self._S_rect)
		self.screen.blit(self._K, self._K_rect)
		self.screen.blit(self._L, self._L_rect)

		pygame.draw.rect(self.screen, self.settings.BG_COLOR, (0, 0, self.settings.WIDTH, 24))
		pygame.draw.line(self.screen, BLACK, (0, 24), (self.settings.WIDTH, 24), 2)
		self.screen.blit(self._score, self._score_rect)
		if self.perfect_game:
			self.screen.blit(self.star, self.star_rect)

		if not self._play:
			pygame.draw.rect(self.screen, WHITE, (50, 200, 300, 300))
			pygame.draw.rect(self.screen, BLACK, (50, 200, 300, 300), 2)

			if self._easy_hover:
				pygame.draw.rect(self.screen, RED, self._easy_button)
			else:
				pygame.draw.rect(self.screen, GRAY, self._easy_button)

			if self._medium_hover:
				pygame.draw.rect(self.screen, GREEN, self._medium_button)
			else:
				pygame.draw.rect(self.screen, GRAY, self._medium_button)

			if self._hard_hover:
				pygame.draw.rect(self.screen, BLUE, self._hard_button)
			else:
				pygame.draw.rect(self.screen, GRAY, self._hard_button)

			self.screen.blit(self._piano_tiles, self._piano_tiles_rect)
			self.screen.blit(self._select, self._select_rect)
			self.screen.blit(self._easy, self._easy_rect)
			self.screen.blit(self._medium, self._medium_rect)
			self.screen.blit(self._hard, self._hard_rect)

		if self._lose:
			pygame.draw.rect(self.screen, WHITE, (50, 200, 300, 300))
			pygame.draw.rect(self.screen, BLACK, (50, 200, 300, 300), 2)

			if self._playagain_hover:
				pygame.draw.rect(self.screen, GREEN, self._playagain_button)
			else:
				pygame.draw.rect(self.screen, GRAY, self._playagain_button)

			if self._quit_hover:
				pygame.draw.rect(self.screen, RED, self._quit_button)
			else:
				pygame.draw.rect(self.screen, GRAY, self._quit_button)

			self.screen.blit(self._yourscore, self._yourscore_rect)
			self.screen.blit(self._score_plus_bonus, self._score_plus_bonus_rect)
			self.screen.blit(self._finalscore, self._finalscore_rect)
			self.screen.blit(self._playagain, self._playagain_rect)
			self.screen.blit(self._quit, self._quit_rect)


		pygame.display.flip()

	def run(self):
		frames = 0
		step = 100
		while True:
			self.clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					print(f'Your score: {self.score}')
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						print(f'Your score: {self.score}')
						sys.exit()

					if self._play:
						if event.key == pygame.K_a:
							try:
								if self.cols[0][0].rect.collidepoint(50, self.settings.HEIGHT - 100):
									self.cols[0].pop(0)
									self.score += step
								else:
									self.score -= step
									self.perfect_game = False
							except:
								self.score -= step
								self.perfect_game = False

						if event.key == pygame.K_s:
							try:
								if self.cols[1][0].rect.collidepoint(150, self.settings.HEIGHT - 100):
									self.cols[1].pop(0)
									self.score += step
								else:
									self.score -= step
									self.perfect_game = False
							except:
								self.score -= step
								self.perfect_game = False

						if event.key == pygame.K_k:
							try:
								if self.cols[2][0].rect.collidepoint(250, self.settings.HEIGHT - 100):
									self.cols[2].pop(0)
									self.score += step
								else:
									self.score -= step
									self.perfect_game = False
							except:
								self.score -= step
								self.perfect_game = False

						if event.key == pygame.K_l:
							try:
								if self.cols[3][0].rect.collidepoint(350, self.settings.HEIGHT - 100):
									self.cols[3].pop(0)
									self.score += step
								else:
									self.score -= step
									self.perfect_game = False
							except:
								self.score -= step
								self.perfect_game = False

				if event.type == pygame.MOUSEBUTTONDOWN:
					if self._lose:
						if self._playagain_hover:
							self.cols = [[], [], [], []]
							self.score = 0
							self._lose = False
							self.perfect_game = True
						if self._quit_hover:
							sys.exit()

					else:
						if self._easy_hover:
							self.tile_vel = 5
							self._play = True
						if self._medium_hover:
							self.tile_vel = 10
							self._play = True
						if self._hard_hover:
							self.tile_vel = 20
							self._play = True

			if self._play:
				if frames > 60:
					if frames % (200 // self.tile_vel) == 0:
						if random() < 0.23:
							self.cols[0].append(Tile(0, -200))

						if random() < 0.23:
							self.cols[1].append(Tile(100, -200))

						if random() < 0.23:
							self.cols[2].append(Tile(200, -200))

						if random() < 0.23:
							self.cols[3].append(Tile(300, -200))

					for col in self.cols:
						for tile in col:
							tile.rect.y += self.tile_vel

				for col in self.cols:
					for tile in col:
						if tile.rect.colliderect(self._bottom_rect):
							self._lose = True
							self._play = False

							if self.perfect_game and self.score >= 5000:
								self._score_plus_bonus = self.font.render(f'{int(self.score)} + {int(self.score // 2)}', True, BLACK)
								self.score *= 1.5
							else:
								self._score_plus_bonus = self.font.render(f'{int(self.score)} + 0', True, BLACK)

							self._score_plus_bonus_rect = self._score_plus_bonus.get_rect()
							self._score_plus_bonus_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2 - 50)

							self._finalscore = self.big_font.render(f'{int(self.score)}', True, BLACK)
							self._finalscore_rect = self._finalscore.get_rect()
							self._finalscore_rect.center = (self.settings.WIDTH // 2, self.settings.HEIGHT // 2)

				self._score = self.font.render(f'{int(self.score)}', True, BLACK)
				self._score_rect = self._score.get_rect()
				self._score_rect.center = (self.settings.WIDTH // 2, 12)

				frames += 1

			elif not self._lose:
				mouse_pos = pygame.mouse.get_pos()

				if self._easy_button.collidepoint(mouse_pos):
					self._easy_hover = True
				else:
					self._easy_hover = False

				if self._medium_button.collidepoint(mouse_pos):
					self._medium_hover = True
				else:
					self._medium_hover = False

				if self._hard_button.collidepoint(mouse_pos):
					self._hard_hover = True
				else:
					self._hard_hover = False

			else:
				mouse_pos = pygame.mouse.get_pos()

				if self._playagain_button.collidepoint(mouse_pos):
					self._playagain_hover = True
				else:
					self._playagain_hover = False

				if self._quit_button.collidepoint(mouse_pos):
					self._quit_hover = True
				else:
					self._quit_hover = False

			self.draw()

				
if __name__ == '__main__':
	game = Game()
	game.run()