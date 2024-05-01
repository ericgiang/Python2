# Name: Starter Code
# Description: Porting A5 to Python
# Date: Spring 2024

import pygame
import time
import json

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, x, y, w, h, image):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.image = pygame.image.load(image) 

	##methods for checking which sprite 
	def is_wall(self):
		return False
	
	def is_pacman(self):
		return False
	
	def is_fruit(self):
		return False
	
	def is_ghost(self): 
		return False
	
	def is_pellet(self):
		return False
	
	##methods for checking behavior of sprites
	def is_moving(self):
		return False
	def update(self):
		pass

	##Getters and Setters
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getW(self):
		return self.w
	def getH(self):
		return self.h
	
	##Other methods of our Sprite class
	def does_collide(self, other_sprite):
		return not (self.x + self.w < other_sprite.x or self.x > other_sprite.x + other_sprite.x
			  or self.y + self.h < other_sprite.y or self.y > other_sprite.y + other_sprite.h)

	def draw(self, screen, cameraY):
			screen.blit(pygame.transform.scale(self.image, (self.w, self.h)), (self.x, (self.y - cameraY)))

		

class Wall(Sprite):
	def __init__(self, x, y, w, h):
		super().__init__(x, y, w, h, "wall.png")
	
	def is_wall(self):
		return True
	
	def is_moving(self):
		return False
	
	def update(self):
		return True

	##Getters and Setters
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getW(self):
		return self.w
	def getH(self):
		return self.h

class Pacman(Sprite):
	def __init__(self, x, y):
		super().__init__(x, y, 35, 35, "zeldaImages/zelda1.png")
		self.zeldaImages = []
		self.currentImage = 0
		self.direction = 0
		self.prevsX = 0
		self.prevY = 0
		self.isValid = True
		self.moving = False
		self.load_images()
		self.animationCounter = 0
		self.isValid = True
		self.speed = 5
	# def move(self, x, y):
	# 	self.x += x
	# 	self.y += y
	#Methods Pacman will override
	def update(self):
		return self.isValid
	
	def is_moving(self):
		return True
	
	def is_pacman(self):
		return True
	
	def move(self):
		if self.direction == 0: #Down 
			self.y += self.speed
		elif self.direction == 1: #Left
			self.x -= self.speed
		elif self.direction == 2: #Right
			self.x += self.speed
		elif self.direction == 3: #Up
			self.y -= self.speed
	
	def load_images(self):
		for i in range(1, 13):  # Load images zelda1.png to zelda12.png
			image = pygame.image.load(f"zeldaImages/zelda{i}.png")
			self.zeldaImages.append(image)
			
	def draw(self, screen, cameraY):
		if len(self.zeldaImages) == 12:  # Check if all images are loaded
			imageIndex = self.currentImage + self.direction * 3
			current_image = self.zeldaImages[imageIndex]
			screen.blit(pygame.transform.scale(current_image, (self.w, self.h)), (self.x, (self.y - cameraY)))

	def update_current_image(self):
		if self.moving:
			self.currentImage = (self.currentImage + 1) % 3

class Model():
	def __init__(self):
		self.sprites = []
		# self.sprites.append(Wall(200,100,51,46))
		self.zelda = Pacman(0, 0)
		self.sprites.append(self.zelda)
		
		#open the json map and pull out the individual lists of sprite objects
		with open("map.json") as file:
			data = json.load(file)
			#get the list labeled as "lettuces" from the map.json file
			walls = data["Walls"]
		file.close()
		
		#for each entry inside the lettuces list, pull the key:value pair out and create 
		#a new Lettuce object with (x,y,w,h)
		for entry in walls:
			self.sprites.append(Wall(entry["x"], entry["y"], entry["w"], entry["h"]))

	def update(self):
		for sprite in self.sprites:
			sprite.update()

	# def moveTurtle(self, x, y):
	# 	self.turtle.move(x, y)

class View():
	def __init__(self, model):
		screen_size = (600,800)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model

	def update(self):
		self.screen.fill([0,200,100])
		for sprite in self.model.sprites:
			LOCATION = (sprite.x, sprite.y)
			SIZE = (sprite.w, sprite.h)
			self.screen.blit(pygame.transform.scale(sprite.image, SIZE), LOCATION)
		pygame.display.flip()

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keep_going = True
		self.key_right = False
		self.key_left = False
		self.key_down = False
		self.key_up = False
	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					self.keep_going = False
				elif event.key == K_RIGHT: 
					self.key_right = True
					self.model.zelda.moving = True
				elif event.key == K_LEFT: 
					self.key_left = True
					self.model.zelda.moving = True
				elif event.key == K_DOWN: 
					self.key_down = True
					self.model.zelda.moving = True
				elif event.key == K_UP: 
					self.key_up = True
					self.model.zelda.moving = True

			elif event.type == pygame.MOUSEBUTTONUP:
				#this function is included to you to see how mouse presses are 
				#handled in Python. setDestination is no longer provided since 
				#you should not have that in your final product!
				pass
			elif event.type == pygame.KEYUP: #this is keyReleased!
				pass
				if event.key == K_RIGHT:
					self.key_right = False
				elif event.key == K_LEFT:
					self.key_left = False
				elif event.key == K_DOWN:
					self.key_down = False
				elif event.key == K_UP:
					self.key_up = False
			
		keys = pygame.key.get_pressed()
		moving = keys[K_RIGHT] or keys[K_LEFT] or keys[K_DOWN] or keys[K_UP]
		self.model.zelda.moving = moving  # Update the moving state
		if keys[K_RIGHT]:
			self.model.zelda.direction = 2
			self.model.zelda.move()
		if keys[K_LEFT]:
			self.model.zelda.direction = 1
		if keys[K_DOWN]:
			self.model.zelda.direction = 0
			self.model.zelda.move()
		if keys[K_UP]:
			self.model.zelda.direction = 3
			self.model.zelda.move()

		if self.model.zelda.moving:
			self.model.zelda.update_current_image()

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")