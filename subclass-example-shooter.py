from scene import *
import sound
import random
import math
A = Action


class Shooter(SpriteNode):
	
	def __init__(self, max_bullets, display_bar=True, **kwargs):
		
		# call super initializer and pass on keyword arguments
		super().__init__(**kwargs)
		# save arguments as attributes of object
		self.max_bullets = max_bullets
		self.bullets = max_bullets
		
		# set container rectangle to zero size
		self.size = (0, 0)
		
		# create face SN
		self.face = SpriteNode('emj:Grinning', parent=self)

		# create gun SN
		self.gun = SpriteNode('spc:Gun4', scale=1.2, z_position=-1, parent=self)
		# set anchor point to middle bottom, rotation is around anchor point
		self.gun.anchor_point = (0.5, 0)
		
		# create rotation action and apply it to gun
		spin_forever = A.repeat_forever(A.rotate_by(math.radians(360), 10))
		self.gun.run_action(spin_forever)
		
		# create action to replenish bullets - half second wait in between each addition
		# use A.call to create action onject that calls another method or function
		repl_bullets = A.repeat_forever(A.sequence(A.wait(0.5), A.call(self.add_bullets)))
		self.run_action(repl_bullets)
		
		# create bullets bar using multiple nested SpriteNodes
		white_box = SpriteNode(color='white', position=(0, -70), size=(60,10), parent=self)
		black_box = SpriteNode(color='black', size=(59,9), parent=white_box)
		# create bullets_bar as attribute of object to use in other methods
		self.bullets_bar = SpriteNode(color='#0f24ff', position=(-29, -4), size=(58,8), parent=white_box)
		# set anchor point so bar fill will stick to left side
		self.bullets_bar.anchor_point = (0, 0)
		# hide white box and all sub nodes when display_bar False is passed to __init__()
		if display_bar == False:
			white_box.alpha = 0
		

	def add_bullets(self, num_to_add=1):
		# check to see if bullet can be added, default is 1
		if self.bullets + num_to_add <= self.max_bullets:
			self.bullets = self.bullets + num_to_add
			# set bar to correct width
			self.bullets_bar.x_scale = self.bullets / self.max_bullets
			# set bar color to red if <= 25%
			if self.bullets_bar.x_scale <= 0.25:
				self.bullets_bar.color = 'red'
			else:
				self.bullets_bar.color = '#0f24ff'	
	
	def fire_bullet(self):
		# check that we have a bullet to fire
		if self.bullets > 0:	
			# subtract 1 bullet by adding negative 1
			self.add_bullets(-1)
			sound.play_effect('arcade:Laser_1')
			# create new bullet, z position set to -2 to be behind face and gun
			new_bullet = SpriteNode('spc:LaserBlue10', z_position=-2, parent=self)
			# set rotation of bullet to match gun angle
			new_bullet.rotation = self.gun.rotation
			# create movement action based on sin and cos, remove bullet from screen after movement is finished
			move_bullet = A.sequence(A.move_by(-1000*math.sin(new_bullet.rotation), 1000*math.cos(new_bullet.rotation)), A.remove())
			new_bullet.run_action(move_bullet)
	
	# override __str__ method, mainly used for providing meaningful info when printing object during debugging
	def __str__(self):
		return 'Shooter object with bullets ' + str(self.bullets) + ' and max bullet limit ' + str(self.max_bullets)
	

	
		
				
class MyScene (Scene):
	def setup(self):
		
		# create tom Shooter object with 10 max bullets
		self.tom = Shooter(10, position=(200,300), parent=self)

		# create bob Shooter object with 100 max bullets and display_bar keyword argument set to False to hide the bullets bat
		self.bob = Shooter(100, display_bar=False, position=(600,300), parent=self)
		# change face from defaultto Frog by accessing face attribute of Shooter object
		self.bob.face.texture = Texture('emj:Frog_Face')

		# Create 2 buttons, one for each Shooter
		self.button_1 = SpriteNode('iow:ios7_circle_filled_256', position=(100,100), parent=self, scale=0.5, color='#ff1e1e')
		self.button_2 = SpriteNode('iow:ios7_circle_filled_256', position=(650,100), parent=self, scale=0.5)
		
	
	def update(self):
		pass
	
	def touch_began(self, touch):
		
		# button handling for tom and bob Shooter objects
		if touch.location in self.button_1.bbox:
			self.tom.fire_bullet()
			# print all object attributes as dictionary
			#print(vars(self.tom))
		elif touch.location in self.button_2.bbox:
			self.bob.fire_bullet()
		
	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass

if __name__ == '__main__':
	run(MyScene(), show_fps=False)
