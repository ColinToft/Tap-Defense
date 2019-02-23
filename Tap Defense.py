from scene import *
from sound import load_effect, play_effect, stop_effect
from random import shuffle, randint
from time import time
import shelve

class Main (Scene):
	def setup(self):
		self.state = 'Menu'
		self.maxSpeed = 60
		with shelve.open('TapDefenseSave') as save:
			if 'Highscores' not in save:
				save['Highscores'] = {'YOLO': 0, 'Have Fun': 0}
				
			self.highscores = save['Highscores']
			
		self.sounds = [
		'Piano_G4#', 'Piano_F4', 'Piano_D4#', 'Piano_G3#',
		'Piano_C4', 'Piano_C4#', 'Piano_G4' 'Coin_3', 'Error'
		]
		for i in self.sounds:
			load_effect(i)
			
		self.music = {
		1: 'G4#', 13: 'G4#', 25: 'F4', 37: 'D4#', 43: 'G4#', 97: 'G4#',
		109: 'G4#', 121: 'F4', 133: 'D4#', 139: 'G4#', 193: 'G4#',
		205: 'G4#', 217: 'G3#', 229: 'G3#', 241: 'G4#', 253: 'G4#',
		265: 'G3#', 277: 'C4', 289: 'D4#', 313: 'C4#', 337: 'C4', 361: 'G4'
		}
		
		self.all_images = [
		'Ant', 'Baby_Chick_1', 'Baby_Chick_2', 'Baby_Chick_3', 'Bactrian_Camel',
		'Bear_Face', 'Bird', 'Blowfish', 'Boar', 'Bug', 'Cat_Face_Crying',
		'Cat_Face_Grinning', 'Cat_Face_Heart-Shaped_Eyes', 'Cat_Face_Kissing',
		'Cat_Face_Pouting', 'Cat_Face_Smiling', 'Cat_Face_Weary',
		'Cat_Face_With_Tears_Of_Joy', 'Cat_Face_With_Wry_Smile', 'Cat_Face', 'Chicken',
		'Cow_Face', 'Dog_Face', 'Dolphin', 'Elephant', 'Fish', 'Frog_Face', 'Hamster_Face',
		'Honeybee', 'Horse_Face', 'Horse', 'Koala', 'Lady_Beetle', 'Monkey_Face',
		'Monkey_Hear-No-Evil', 'Monkey_See-No-Evil', 'Monkey_Speak-No-Evil', 'Monkey',
		'Mouse_Face', 'Octopus', 'Panda_Face', 'Penguin', 'Pig_Face', 'Pig_Nose',
		'Pile_Of_Poo', 'Poodle', 'Rabbit_Face', 'Sheep', 'Snail', 'Snake', 'Spiral_Shell',
		'Tiger_Face', 'Tropical_Fish', 'Turtle', 'Whale', 'Wolf_Face'
		]
		
		self.f = 'Futura'
		self.instrF = 'DejaVuSansMono'
		self.scoreF = 'ChalkboardSE-Regular'
		
		self.smallS = 20
		self.s = 30
		self.largeS = 40
		self.titleS = 50
		
		self.ipad = self.size.w > 400
		if self.ipad:
			self.smallS *= 1.5
			self.s *= 1.5
			self.largeS *= 1.5
			self.titleS *= 1.5
			
	def startGame(self, mode):
		sw = self.size.w * 0.25
		self.buttons = []
		shuffle(self.all_images)
		images_used = self.all_images[:4]
		for i in range(4):
			self.buttons.append(Layer(Rect(i * sw, 0, sw, sw)))
			self.buttons[i].image = images_used[i]
			
		self.speed = 1 if mode == 'YOLO' else 30
		self.music_frame = 0
		self.prevEffect = None
		self.assigned = False
		self.imagesOnScreen = []
		self.startTime = time()
		self.state = mode
		
	def endGame(self):
		self.time = time() - self.startTime
		play_effect('Error')
		self.highscoreText = self.time > self.highscores[self.state]
		if self.highscoreText:
			self.highscores[self.state] = self.time
			
		self.state += ' Win'
		
	def draw(self):
		w = self.size.w
		h = self.size.h
		sw = w * 0.25
		
		if self.state == 'Menu':
			background(0.75, 1, 0)
			tint(0, 0, 0)
			text('Tap Defense', 'BanglaSangamMN', self.titleS, w * 0.5, h * 0.8)
			text('YOLO', self.scoreF, self.largeS, w * 0.5, h * 0.5)
			text('Have Fun...', self.scoreF, self.largeS, w * 0.5, h * 0.35)
			text('Highscores', self.scoreF, self.largeS, w * 0.5, h * 0.2)
			
		elif self.state in ['YOLO', 'Have Fun']:
			background(0, 0, 0)
			
			if self.music_frame in self.music:
				if self.prevEffect: stop_effect(self.prevEffect)
				self.prevEffect = play_effect('Piano_' + self.music[self.music_frame])
			self.music_frame = (self.music_frame + 1) % 384
			
			for i in self.buttons:
				i.update(self.dt)
				i.draw()
				
			fill(1, 1, 1)
			rect(0, sw, w, 1)
			for i in range(1, 4):
				rect(sw * i, 0, 1, sw)
				
			for image in self.imagesOnScreen:
				image.frame = image.frame.translate(0, -self.speed)
				if image.frame.y <= sw:
					self.imagesOnScreen.remove(image)
					self.endGame()
					
				image.update(self.dt)
				image.draw()
				
			if randint(0, self.maxSpeed * 2) < self.speed:
				x = randint(0, 3) * sw
				image = self.buttons[randint(0, 3)].image
				if not any(Rect(x, h - sw, sw, sw).intersects(i.frame) for i in self.imagesOnScreen):
					layer = Layer(Rect(x, h - sw, sw, sw))
					layer.image = image
					self.imagesOnScreen.append(layer)
					
			self.speed = min(self.speed + 0.001, self.maxSpeed)
			
		elif self.state.startswith('Starting'):
			background(0, 0, 0)
			tint(1, 1, 1)
			text('YOLO Mode' if self.state == 'Starting YOLO' else 'Have Fun...', self.f, self.titleS, w * 0.5, h * 0.9)
			text('How to play:', self.instrF, self.s, w * 0.5, h * 0.75)
			text('When a picture falls down', self.instrF, self.smallS, w * 0.5, h * 0.67)
			text('from the top of the screen,', self.instrF, self.smallS, w * 0.5, h * 0.63)
			text('tap on its corresponding', self.instrF, self.smallS, w * 0.5, h * 0.59)
			text('image on the bottom to', self.instrF, self.smallS, w * 0.5, h * 0.55)
			text('make it dissappear. If an', self.instrF, self.smallS, w * 0.5, h * 0.51)
			text('image makes it to the', self.instrF, self.smallS, w * 0.5, h * 0.47)
			text('bottom, you lose the game.', self.instrF, self.smallS, w * 0.5, h * 0.43)
			text('Tap to start!', self.f, self.titleS, w * 0.5, h * 0.12)
			
		elif self.state.endswith('Win'):
			background(0, 0, 0)
			text('New Highscore!' if self.highscoreText else 'You lost!', self.f, self.largeS, w * 0.5, h * 0.9)
			text('Time:', self.scoreF, self.titleS, w * 0.5, h * 0.5)
			text(str(int(self.time)) + ' seconds', self.scoreF, self.largeS, w * 0.5, h * 0.45)
			text('Menu', self.f, self.smallS, w - 5, 5, alignment=7)
			
		elif self.state == 'Highscores':
			background(0, 0, 0)
			tint(1, 1, 1)
			text('Highscores', self.f, self.largeS, w * 0.5, h * 0.9)
			text('YOLO Mode:', self.f, self.largeS, w * 0.5, h * 0.55)
			text(str(int(self.highscores['YOLO'])) + ' seconds', self.f, self.s, w * 0.5, h * 0.5)
			text('Have Fun Mode:', self.f, self.largeS, w * 0.5, h * 0.35)
			text(str(int(self.highscores['Have Fun'])) + ' seconds', self.f, self.s, w * 0.5, h * 0.3)
			text('Menu', self.f, self.smallS, w - 5, 5, alignment=7)
			
	def touch_began(self, touch):
		w = self.size.w
		h = self.size.h
		l = touch.location
		
		def touchingText(x, y, width, height):
			if self.ipad:
				width *= 1.5
				height *= 1.5
			return l in Rect(w * x - width / 2, h * y - height / 2, width, height)
			
		if self.state == 'Menu':
			if touchingText(0.5, 0.5, 100, 60):
				self.state = 'Starting YOLO'
			elif touchingText(0.5, 0.35, 100, 60):
				self.state = 'Starting Have Fun'
			elif touchingText(0.5, 0.2, 100, 60):
				self.state = 'Highscores'
				
		elif self.state.startswith('Starting'):
			self.startGame(self.state[9:])
			
		elif self.state in ['YOLO', 'Have Fun']:
			sw = w * 0.25
			if l in Rect(0, 0, w, sw):
				buttonPressed = int(l.x / sw)
				
				if any(i.image == self.buttons[buttonPressed].image for i in self.imagesOnScreen):
					play_effect('Coin_3')
					for i in self.imagesOnScreen:
						if i.image == self.buttons[buttonPressed].image:
							self.imagesOnScreen.remove(i)
							return
				else:
					self.endGame()
					
		elif self.state.endswith('Win') or self.state == 'Highscores':
			if touchingText(0.85, 0.05, 100, 60):
				self.state = 'Menu'
				
	def pause(self):
		self.save()
		
	def stop(self):
		self.save()
		
	def save(self):
		with shelve.open('TapDefenseSave') as save:
			save['Highscores'] = self.highscores
			
run(Main(), PORTRAIT)

