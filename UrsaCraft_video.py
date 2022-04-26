from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()
# grass_texture = load_texture('assets/grass_block.png')
# stone_texture = load_texture('assets/stone_block.png')
# brick_texture = load_texture('assets/brick_block.png')
# dirt_texture  = load_texture('assets/dirt_block.png')
# sky_texture   = load_texture('assets/skybox.png')
# arm_texture   = load_texture('assets/arm_texture.png')
grass_texture = 'assets/grass_block.png'
stone_texture = 'assets/stone_block.png'
brick_texture = 'assets/brick_block.png'
dirt_texture  = 'assets/dirt_block.png'
sky_texture   = 'assets/skybox.png'
arm_texture   = 'assets/arm_texture.png'
punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
bg_sound = Audio('assets/bg.mp3', loop = True, autoplay = True)
walking_sound = Audio("assets/walking.mp3", loop = True, autoplay = False)
walking_play_called = False
block_pick = 1

player = FirstPersonController()

# window.fps_counter.enabled = False
# window.exit_button.visible = False

def update():
	global block_pick

	if held_keys['left mouse'] or held_keys['right mouse']:
		hand.active()
	else:
		hand.passive()

	if held_keys['1']: block_pick = 1
	if held_keys['2']: block_pick = 2
	if held_keys['3']: block_pick = 3
	if held_keys['4']: block_pick = 4

	if player.position.y < -25:
		player.position = (0, 0.25, 0)
		print("below")
	

def input(key):
	global walking_play_called
	if held_keys[Keys.escape]:
		mouse.locked = False
		mouse.visible = True
	if key == Keys.left_mouse_down:
		mouse.locked = True
		mouse.visible = False
	if held_keys["h"]:
		print(f"Player: {player.position}")
	if (held_keys["w"] or held_keys["s"] or held_keys["a"] or held_keys["d"]) and walking_sound.playing == False:
		print("played")
		if	walking_play_called == False:
			walking_play_called = True
			walking_sound.play()
		else:
			walking_sound.resume()
	if (not held_keys["w"] and not held_keys["s"] and not held_keys["a"] and not held_keys["d"]) and walking_sound.playing == True:
		print("Paused")
		walking_sound.pause()

class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5)

	def input(self,key):
		if self.hovered:
			if key == 'left mouse down':
				punch_sound.play()
				pos = self.position + mouse.normal
				if block_pick == 1: 
					voxel = Voxel(position = pos, texture = grass_texture)
					self.save_block(1, grass_texture, pos)
					print(f"Texture: {voxel.texture}, Position: {pos.x}, {pos.y}, {pos.z}")
				if block_pick == 2: 
					voxel = Voxel(position = pos, texture = stone_texture)
					self.save_block(1, stone_texture, pos)
					print(f"Texture: {voxel.texture}, Position: {pos.x}, {pos.y}, {pos.z}")
				if block_pick == 3: 
					voxel = Voxel(position = pos, texture = brick_texture)
					self.save_block(1, brick_texture, pos)
					print(f"Texture: {voxel.texture}, Position: {pos.x}, {pos.y}, {pos.z}")
				if block_pick == 4: 
					voxel = Voxel(position = pos, texture = dirt_texture)
					self.save_block(1, dirt_texture, pos)
					print(f"Texture: {voxel.texture}, Position: {pos.x}, {pos.y}, {pos.z}")

			if key == 'right mouse down':
				punch_sound.play()
				self.save_block(0, self.texture, self.position)
				destroy(self)
				

	# action: action == 1, which means add a block, action == 0, remove a block
	def save_block(self, action, texture, position):
		# block_type and position to a file
		history = open("./oscar.txt", "a")
		history.write(f"{action},{texture},{position.x},{position.y},{position.z}\n")
		history.close()

class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 300,
			double_sided = True)

class Hand(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'assets/arm',
			texture = arm_texture,
			scale = 0.2,
			rotation = Vec3(150,-10,0),
			position = Vec2(0.4,-0.6))

	def active(self):
		self.position = Vec2(0.3,-0.5)

	def passive(self):
		self.position = Vec2(0.4,-0.6)

for z in range(50):
	for x in range(50):
		voxel = Voxel(position = (x,0,z))

try:
	history = open("./oscar.txt", "r")
	line = history.readline()
	while line != "":
		fields = line.split(",")
		# action
		action = int(fields[0])
		# texture
		texture = fields[1]
		# x, y, z
		x = float(fields[2])
		y = float(fields[3])
		z = float(fields[4])
		if action == 1:
			voxel = Voxel(position = Vec3(x, y, z), texture = texture)
		else:
			ens = scene.entities
			for en in ens:
				if en.position.x != x or en.position.y != y or en.position.z != z:
					continue
				destroy(en)
				break
		line = history.readline()
	history.close()
except IOError:
	print("No history file")


sky = Sky()
hand = Hand()

app.run()