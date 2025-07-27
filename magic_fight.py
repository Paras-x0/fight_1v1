import sys
import pygame
import random

from health import HealthBar 
from evil_wizard import Evil_wizard
from hero_knight import Hero_knight
from martial_hero import Martial_hero

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption('Magic Fight')

# images used in character selection
wizard_img = pygame.image.load("EvilWizard_idle/idle_frame_0.png").convert_alpha()
wizard_img = pygame.transform.scale(wizard_img, (300, 300))
knight_img = pygame.image.load('HeroKnight_idle/idle_frame_0.png').convert_alpha()
knight_img = pygame.transform.scale(knight_img, (300, 300))
martial_img = pygame.image.load('MartialHero_idle/idle_frame_0.png').convert_alpha()
martial_img = pygame.transform.scale(martial_img, (300, 300))
wizard_rect = wizard_img.get_rect(center=(300, 300))
knight_rect = knight_img.get_rect(center=(640, 300))
martial_rect = martial_img.get_rect(center=(980, 300))

# Background
sky_surface = pygame.image.load('surfaces/sky.png').convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (1280, 500))
land_surface = pygame.image.load('surfaces/terrain_strip_1.png').convert_alpha()

#see all types of font i have used 
title_font = pygame.font.Font('assets/Pixel Game.otf', 50)
button_font = pygame.font.Font('assets/Pixel Game.otf', 30)

#buttons for mode selections
VS_player = pygame.Rect(300, 300, 220, 50)
# VS_computer = pygame.Rect(600, 300, 220, 50)

# Health bars
Health_bar = HealthBar(25, 30, 500, 30, 100)
Health_bar1 = HealthBar(750, 30, 500, 30, 100)


# music
bg_music = pygame.mixer.Sound('assets/electricguitar.mp3')
bg_music.set_volume(0.4)
bg_music.play()


game_state = "intro"
selected_character = None
selected_mode = None
selected_character2 = None
all_sprites = None

running = True
while running:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()


		if event.type == pygame.KEYDOWN and game_state == "intro":
			game_state = "character_selection"
		elif game_state == "character_selection":
			if event.type == pygame.MOUSEBUTTONDOWN:
				if wizard_rect.collidepoint(event.pos):
					selected_character = "wizard"
					game_state = "mode_selection"
				elif knight_rect.collidepoint(event.pos):
					selected_character = "knight"
					game_state = "mode_selection"
				elif martial_rect.collidepoint(event.pos):
					selected_character = "martial"
					game_state = "mode_selection"


		elif game_state == "mode_selection":
			if event.type ==pygame.MOUSEBUTTONDOWN:
				if player_text_rect.collidepoint(event.pos):
					selected_mode = "pvp"
					game_state = "character_selection2"
					state_entry_time = pygame.time.get_ticks()

		elif game_state == "character_selection2":
			if event.type == pygame.MOUSEBUTTONDOWN:
				if wizard_rect.collidepoint(event.pos):
					selected_character2 = "wizard"
				elif knight_rect.collidepoint(event.pos):
					selected_character2 = "knight"
				elif martial_rect.collidepoint(event.pos):
					selected_character2 = "martial"

				if selected_character2:
					
					if selected_character == "wizard":
						player1 = Evil_wizard(Health_bar, spawn_side="left")
					elif selected_character == "knight":
						player1 = Hero_knight(Health_bar, spawn_side="left")
					elif selected_character == "martial":
						player1 = Martial_hero(Health_bar, spawn_side="left")

					
					if selected_character2 == "wizard":
						player2 = Evil_wizard(Health_bar1, spawn_side="right")
					elif selected_character2 == "knight":
						player2 = Hero_knight(Health_bar1, spawn_side="right")
					elif selected_character2 == "martial":
						player2 = Martial_hero(Health_bar1, spawn_side="right")

					
					all_sprites = pygame.sprite.Group(player1, player2)
					game_state = "playing"
					state_entry_time = pygame.time.get_ticks()





	if game_state == "intro":
		screen.blit(sky_surface , (0,0))
		screen.blit(land_surface , (0 , 450))
		title_text = title_font.render("press any key to start" , False, (0,255,0))
		screen.blit(title_text , (400,300))



	elif game_state == "character_selection":
		screen.blit(sky_surface , (0,0))
		screen.blit(land_surface , (0 , 450))
		screen.blit(wizard_img , wizard_rect)
		screen.blit(knight_img , knight_rect)
		screen.blit(martial_img , martial_rect)

		if selected_character == "wizard":
			pygame.draw.rect(screen , (0,255,0) , wizard_rect , 5)
		elif selected_character == "knight":
			pygame.draw.rect(screen , (0,255,0) , knight_rect , 5)
		elif selected_character == "martial":
			pygame.draw.rect(screen , (0,255,0) , martial_rect , 5)

	elif game_state == "character_selection2":
		screen.blit(sky_surface , (0,0))
		screen.blit(land_surface , (0 , 450))
		screen.blit(wizard_img , wizard_rect)
		screen.blit(knight_img , knight_rect)
		screen.blit(martial_img , martial_rect)

		if selected_character2 == "wizard":
			pygame.draw.rect(screen , (0,255,0) , wizard_rect , 5)
		elif selected_character2 == "knight":
			pygame.draw.rect(screen , (0,255,0) , knight_rect , 5)
		elif selected_character2 == "martial":
			pygame.draw.rect(screen , (0,255,0) , martial_rect , 5)

	elif game_state == "mode_selection":
		screen.blit(sky_surface , (0,0))
		screen.blit(land_surface , (0 , 450))
		
		pygame.draw.rect(screen, (100, 100, 255), VS_player, border_radius=8)
			
		player_text = button_font.render("Player vs Player", False, (0, 0, 0))
		
		player_text_rect = screen.blit(player_text,(320, 310))
		
	elif game_state == "playing":
		screen.blit(sky_surface , (0,0))
		screen.blit(land_surface , (0 , 450))
		for event in events:
			player1.handle_events(event)
			player2.handle_events(event)
			if selected_character == "knight":
				player1.set_gravity(event)
			

		# if selected_mode =="pvc":
		if all_sprites:
			all_sprites.update()
			offset = (player2.rect.x - player1.rect.x, player2.rect.y - player1.rect.y)
			if player1.state == "attack" and not player1.attack_registered and player1.mask.overlap(player2.mask, offset):
				if selected_character == "wizard":
					player2.health_bar.hp -= 15
					player1.attack_registered = True
				else:
					player2.health_bar.hp -= 10
					player1.attack_registered = True

			if player2.state == "attack" and not player2.attack_registered and player2.mask.overlap(player1.mask, offset):
				if selected_character == "wizard":
					player1.health_bar.hp -= 15
					player2.attack_registered = True
				else:
					player1.health_bar.hp -= 10
					player2.attack_registered = True
			all_sprites.draw(screen)


		Health_bar.draw(screen)
		Health_bar1.draw(screen)
		if Health_bar.hp <= 0:
			game_state = "game_over"
		elif Health_bar1.hp <= 0:
			game_state = "game_over"

	elif game_state == "options":
		screen.fill((135, 206, 235))

		# Draw character images
		screen.blit(wizard_img, wizard_rect)
		screen.blit(knight_img, knight_rect)
		screen.blit(martial_img, martial_rect)

		# EVIL WIZARD CONTROLS
		text0 = title_font.render("EVIL WIZARD:", False, (255, 255, 255))
		text1 = title_font.render("A -> Left    D -> Right    R -> hight damage Attack", False, (255, 255, 255))
		# text_1 = title_font.render("this character damage higher damage" , False ,(255, 255, 255) )
		screen.blit(text0, (100, 430))
		screen.blit(text1, (100, 470))

		# HERO KNIGHT CONTROLS
		text2 = title_font.render("HERO KNIGHT:", False, (255, 255, 255))
		text3 = title_font.render("left and right and jump-> Move   Spacebar -> Attack", False, (255, 255, 255))
		screen.blit(text2, (100, 520))
		screen.blit(text3, (100, 560))

		# MARTIAL HERO CONTROLS
		text4 = title_font.render("MARTIAL HERO:", False, (255, 255, 255))
		text5 = title_font.render("Num4 -> Left    Num6 -> Right   Num8 -> teleport    Num0 -> Attack", False, (255, 255, 255))
		screen.blit(text4, (100, 610))
		screen.blit(text5, (100, 650))

		# ESC button
		title_text6 = title_font.render("ESC", False, (255, 255, 255))
		title_rect6 = title_text6.get_rect(topleft=(0, 0))
		screen.blit(title_text6, title_rect6)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if title_rect6.collidepoint(event.pos):
				game_state = "character_selection"



	elif game_state == "game_over":
		screen.blit(sky_surface , (0,0))
		screen.blit(land_surface , (0 , 450))
		# pygame.time.delay(3000)
		# screen.fill(())
		if player1.health_bar.hp == 0:
			text00 =title_font.render("player 2 is winner" , False , (255,255,255))
			text00_rect = text00.get_rect(topleft = (500 , 50))
			screen.blit(text00 , text00_rect)
		elif player2.health_bar.hp == 0:
			text01 =title_font.render("player 1 is winner" , False , (255,255,255))
			text01_rect = text01.get_rect(topleft = (500 , 50))
			screen.blit(text01 , text01_rect)


		pygame.draw.rect(screen , (173, 216, 230), (450 , 200 , 400, 400))
		title_text1 = title_font.render("PLAY" , False, (255,255,255))
		title_rect1 = title_text1.get_rect(topleft = (600 , 250))
		screen.blit(title_text1 , title_rect1)

		title_text2 = title_font.render("QUIT" , False, (255,255,255))
		title_rect2 = title_text2.get_rect(topleft = (600 , 450))
		screen.blit(title_text2 , title_rect2)

		title_text3 = title_font.render("OPTIONS" , False, (255,255,255))
		title_rect3 = title_text3.get_rect(topleft = (600 , 350))
		screen.blit(title_text3 , title_rect3)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if title_rect1.collidepoint(event.pos):
				game_state = "character_selection"
				Health_bar.hp = Health_bar.max_hp
				Health_bar1.hp = Health_bar1.max_hp

			if title_rect3.collidepoint(event.pos):
				game_state = "options"


			if title_rect2.collidepoint(event.pos):
				sys.exit()

	pygame.display.update()

	clock.tick(60)