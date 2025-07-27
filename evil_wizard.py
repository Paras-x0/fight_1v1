import pygame
from health import HealthBar
from fighter_base import FighterBase
class Evil_wizard(FighterBase):
	def __init__(self, health_bar, spawn_side = 'left'):
		super().__init__()

		# ---------- IDLE ----------
		self.idle_frames = []
		for i in range(8):
			img = pygame.image.load(f'EvilWizard_idle/idle_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.idle_frames.append(img)

		# ---------- ATTACK ----------
		self.attack_frame = []
		for i in range(8):
			img = pygame.image.load(f'EvilWizard_attack/attack_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.attack_frame.append(img)

		# ---------- MOVE --------
		self.move_frame = []
		for i in range(8):
			img = pygame.image.load(f'EvilWizard_move/move_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.move_frame.append(img)
		self.attack_registered = False

		self.state = 'idle'
		self.frame_index = 0
		self.animation_speed = 0.2
		self.image = self.idle_frames[self.frame_index]
		self.mask = pygame.mask.from_surface(self.image)
		self.attack_sound = pygame.mixer.Sound('assets/flamethrower.mp3')
		self.attack_sound.set_volume(0.3)

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
		if keys[pygame.K_d]:
			self.rect.x += 5
			self.facing_right = True
		elif keys[pygame.K_a]:
			self.rect.x -= 5
			self.facing_right = False

	def handle_events(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				self.state = 'move'
			elif event.key == pygame.K_a:
				self.state = 'move'
			elif event.key == pygame.K_r:
				self.state = 'attack'
				self.attack_sound.play()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_d or event.key == pygame.K_a or event.key == pygame.K_r:
				self.state = 'idle'

	


	def update(self):
		self.key_down()
		self.boundary_detection()

		self.frame_index += self.animation_speed
		if self.frame_index >= 8:
			self.frame_index = 0
			if self.state == 'attack':
				self.state = 'idle'

			if self.state != "attack":
				self.attack_registered = False

		index = int(self.frame_index)
		if self.state == 'attack':
			img = self.attack_frame[index]
		elif self.state == 'idle':
			img = self.idle_frames[index]
		elif self.state == 'move':
			img = self.move_frame[index]

		if self.facing_right:
			self.image = img
		else:
			self.image = pygame.transform.flip(img, True, False)

		old_center = self.rect.center
		self.rect = self.image.get_rect(center=old_center)

		self.mask = pygame.mask.from_surface(self.image)
