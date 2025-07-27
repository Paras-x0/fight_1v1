import pygame
from health import HealthBar
from fighter_base import FighterBase


class Hero_knight(FighterBase):
	def __init__(self, health_bar , spawn_side = 'left'):
		super().__init__()

		# -------- IDLE --------
		self.idle_frames = []
		for i in range(10):
			img = pygame.image.load(f'HeroKnight_idle/idle_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.idle_frames.append(img)

		# -------- ATTACK --------
		self.attack_frames = []
		for i in range(6):
			img = pygame.image.load(f'HeroKnight_attack/attack_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.attack_frames.append(img)

		# -------- RUN --------
		self.move_frames = []
		for i in range(8):
			img = pygame.image.load(f'HeroKnight_run/move_frame_{i}.png').convert_alpha()
			img = pygame.transform.scale(img, (600, 600))
			self.move_frames.append(img)

		self.attack_registered = False
		self.state = 'idle'
		self.frame_index = 0
		self.animation_speed = 0.2
		self.image = self.idle_frames[self.frame_index]
		self.mask = pygame.mask.from_surface(self.image)
		self.gravity = 0
		self.attack_sound = pygame.mixer.Sound('assets/sword.mp3')
		self.attack_sound.set_volume(0.4)

		GROUND_y = 510

		if spawn_side == "right":
			self.rect = self.image.get_rect(midbottom=(1100, GROUND_y))
			self.facing_right = False
		else:
			self.rect = self.image.get_rect(midbottom=(90 , GROUND_y))
			self.facing_right = True
		self.health_bar = health_bar
		self.facing_right = False


	def boundary_detection(self):
		if self.rect.right >= 1480:
			self.rect.right = 1480
		elif self.rect.left <= -200:
			self.rect.left = -200

	def key_down(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.rect.x += 5
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			self.rect.x -= 5
			self.facing_right = False

	def handle_events(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				self.state = 'move'
			elif event.key == pygame.K_LEFT:
				self.state = 'move'
			elif event.key == pygame.K_SPACE:
				if self.state != "attack":
					self.state = 'attack'
					self.attack_sound.play()
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_SPACE:
				self.state = 'idle'

	def set_gravity(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and self.rect.bottom>= 810:
				self.gravity = -30
				self.state = "jump"

	def apply_gravity(self):
		self.gravity = min(self.gravity + 1, 10)
		self.rect.y += self.gravity
		GROUND_y1 = 810
		if self.rect.bottom >= GROUND_y1:
			self.rect.bottom = GROUND_y1
			self.gravity =0
			if self.state =="jump":
				self.state = "idle"
		elif self.rect.top <= 0:
			self.rect.top = 0


	def update(self):
		self.key_down()
		self.boundary_detection()
		self.apply_gravity()
		
		
		if self.state == 'attack':
			frames = self.attack_frames
		elif self.state == 'move':
			frames = self.move_frames
		elif self.state == "jump":
			frames = self.idle_frames
		else:
			frames = self.idle_frames

		if self.state != "attack":
			self.attack_registered = False

		# update animation
		self.frame_index += self.animation_speed
		if self.frame_index >= len(frames):
			self.frame_index = 0
			if self.state == 'attack':
				self.state = 'idle'  

		
		index = int(self.frame_index)
		img = frames[index]

		if self.state =="jump":
			img = frames[0]
		else:
			img = frames[index]
		
		if self.facing_right:
			self.image = img
		else:
			self.image = pygame.transform.flip(img, True, False)

		
		old_midbottom = self.rect.midbottom
		self.rect = self.image.get_rect(midbottom=old_midbottom)
		self.mask = pygame.mask.from_surface(self.image)