import pygame
from health import HealthBar
from fighter_base import FighterBase
import random


class Martial_hero(FighterBase):
	def __init__(self, health_bar, spawn_side = 'left'):
		super().__init__()

		# ---------- IDLE ----------
		self.idle_frame= []
		for i in range(8):
			img = pygame.image.load(f'MartialHero_idle/idle_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.idle_frame.append(img)

		# ---------- ATTACK ----------
		self.attack_frame = []
		for i in range(6):
			img = pygame.image.load(f'MartialHero_attack/Attack1_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.attack_frame.append(img)

		# ---------- MOVE ----------
		self.move_frame = []
		for i in range(8):
			img = pygame.image.load(f'MartialHero_move/move_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.move_frame.append(img)

		self.state = 'idle'
		self.attack_registered = False
		self.frame_index = 0
		self.animation_speed = 0.2
		self.image = self.idle_frame[self.frame_index]
		self.mask = pygame.mask.from_surface(self.image)
		self.attack_sound = pygame.mixer.Sound('assets/katana.mp3')
		self.attack_sound.set_volume(0.5)
		if spawn_side == "right":
			self.rect = self.image.get_rect(center=(1100, 480))
			self.facing_right = False
		else:
			self.rect = self.image.get_rect(center=(90 , 480))
			self.facing_right = True
		self.health_bar = health_bar
		self.facing_right = True

	def boundary_detection(self):
		if self.rect.right >= 1480:
			self.rect.right = 1480
		elif self.rect.left <= -200:
			self.rect.left = -200

	def key_down(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_KP6]:
			self.rect.x += 5
			self.facing_right = True
		elif keys[pygame.K_KP4]:
			self.rect.x -= 5
			self.facing_right = False

	def handle_events(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_KP6:
				self.state = 'move'
			elif event.key == pygame.K_KP4:
				self.state = 'move'

			elif event.key == pygame.K_KP8:
				self.rect.x = random.randint(0 , 1280)
				self.state = "teleport"

			elif event.key == pygame.K_KP0:
				self.state = 'attack'
				self.attack_sound.play()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_KP6 or event.key == pygame.K_KP4 or event.key == pygame.K_KP0:
				self.state = 'idle'

		

	def update(self):
		self.key_down()
		self.boundary_detection()
	
		
		if self.state == 'attack':
			frames = self.attack_frame
		elif self.state == 'move':
			frames = self.move_frame
		elif self.state == "teleport":
			frames = self.idle_frame
		else:
			frames = self.idle_frame
		if self.state != "attack":
			self.attack_registered = False
		# Update animation frame
		self.frame_index += self.animation_speed
		if self.frame_index >= len(frames):
			self.frame_index = 0
			if self.state == 'attack':
				self.state = 'idle'  

		
		index = int(self.frame_index)
		img = frames[index]

		
		if self.facing_right:
			self.image = img
		else:
			self.image = pygame.transform.flip(img, True, False)

		
		old_center = self.rect.center
		self.rect = self.image.get_rect(center=old_center)
		self.mask = pygame.mask.from_surface(self.image)