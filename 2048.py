import pygame
from sys import exit
from random import choice, random
from math import atan

pygame.init()

square_size = 125
padding = 10
base_font = pygame.font.Font(None, 50)

colors = {
	2: (238, 228, 218),
	4: (238, 225, 201),
	8: (242, 177, 121),
	16:(245, 149, 99),
	32:(246, 124, 95),
	64:(246, 94, 59),
	128:(237, 207, 114),
	256:(237, 204, 97),
	512:(237, 200, 80),
	1024:(237, 197, 63),
	2048:(237, 194, 46),
	4096:(181, 134, 180)
}

text = {2**i: base_font.render(str(2 ** i), False, (0, 0, 0)) for i in range(13)}

def coordinates(position):
	#print(position)
	return (position[1] * (square_size + padding) + padding,
		position[0] * (square_size + padding) + 150)

class Square:

	def __init__(this, position, value):
		this.value = value
		this.position = position
		this.color = pygame.Color(colors[this.value])
		pos = coordinates(position)
		#print(position)
		this.box = pygame.Rect(pos[0], pos[1], square_size, square_size)


	def grow(this):
		this.value *= 2
		this.color = pygame.Color(colors[this.value])
		return this.value

	def show(this):
		pygame.draw.rect(display, this.color, this.box, border_radius=5)
		text_rect = text[this.value].get_rect(center = (this.box.centerx, this.box.centery))
		display.blit(text[this.value], text_rect)

	def __str__(this):
		return f"Square({this.position}, {this.value})"
	
	def __repr__(this):
		return f"Square({this.position}, {this.value})"

class Empty(Square):

	def __init__(this, position):
		this.position = position
		this.color = pygame.Color(205, 193, 180)
		pos = coordinates(position)
		this.box = pygame.Rect(pos[0], pos[1], square_size, square_size)

	def show(this):
		pygame.draw.rect(display, this.color, this.box, border_radius=5)

	def __str__(this):
		return f"Empty({this.position})"	
	
	def __repr__(this):
		return f"Empty({this.position})"	
	
class Grid:
	def __init__(this):
		this.grid = [[Empty((i, j)) for j in range(4)] for i in range(4)]
		this.freeSquares = [(i, j) for i in range(4) for j in range(4)]
		this.movingSquares = []
		this.willFuse = []
		this.score = 0
		this.score_box = base_font.render('Score: 0', False, (0, 0, 0))
		#print(this.grid, this.freeSquares)
		this.createSquare()
		this.createSquare()
		this.show()
		#print(this.grid, this.freeSquares)

	def createSquare(this):
		if this.freeSquares:
			value = 2 if random() < 0.9 else 4
			position = choice(this.freeSquares)
			this.freeSquares.remove(position)
			this.grid[position[0]][position[1]] = Square(position, value)
			#print(this.grid, this.freeSquares)
		else:
			raise Exception("Game Over!")
		
	def move_up(this):
		has_moved = False
		for col in range(4):
			last_taken = -1
			last_grown = -1
			for row in range(4):
				#print(last_taken, this.grid[row][col], this.grid[last_taken][col], (row, col))
				if isinstance(this.grid[row][col], Empty):
					continue
				elif (last_taken == -1 or 
						last_grown == last_taken or
						this.grid[last_taken][col].value != this.grid[row][col].value):
					this.freeSquares.append((row, col))
					if (last_taken + 1, col) in this.freeSquares:
						this.freeSquares.remove((last_taken + 1, col))
					temp = this.grid[row][col]
					this.grid[row][col] = Empty((row, col))
					this.grid[last_taken + 1][col] = temp
					temp.position = (last_taken + 1, col)
					this.movingSquares.append({'square':temp, 'target': coordinates((last_taken + 1, col))})
					last_taken += 1
					if last_taken != row:
						has_moved = True
				else:
					this.freeSquares.append((row, col))
					this.score += this.grid[last_taken][col].grow()
					last_grown = last_taken
					this.score_box = base_font.render(f'Score: {this.score}', False, (0, 0, 0))
					this.willFuse.append(this.grid[row][col])
					this.movingSquares.append({'square':this.grid[row][col], 'target': coordinates((last_taken, col))})
					has_moved = True
		#print(this.freeSquares)
		this.dx = 0
		this.dy = -15
		if has_moved:
			this.createSquare()
		#print(this.freeSquares)
					
	def move_right(this):
		has_moved = False
		for row in range(4):
			last_taken = 4
			last_grown = -1
			for col in range(3, -1, -1):
				#print(last_taken, this.grid[row][col], this.grid[last_taken][col], (row, col))
				if isinstance(this.grid[row][col], Empty):
					continue
				elif (last_taken == 4 or 
						last_grown == last_taken or
						this.grid[row][last_taken].value != this.grid[row][col].value):
					this.freeSquares.append((row, col))
					if (row, last_taken - 1) in this.freeSquares:
						this.freeSquares.remove((row, last_taken - 1))
					temp = this.grid[row][col]
					this.grid[row][col] = Empty((row, col))
					this.grid[row][last_taken - 1] = temp
					temp.position = (row, last_taken - 1)
					this.movingSquares.append({'square':temp, 'target': coordinates((row, last_taken - 1))})
					last_taken -= 1
					if last_taken != col:
						has_moved = True
				else:
					this.freeSquares.append((row, col))
					this.score += this.grid[row][last_taken].grow()
					last_grown = last_taken
					this.score_box = base_font.render(f'Score: {this.score}', False, (0, 0, 0))
					this.willFuse.append(this.grid[row][col])
					this.movingSquares.append({'square':this.grid[row][col], 'target': coordinates((row, last_taken))})
					has_moved = True
		#print(this.freeSquares)
		this.dx = 15
		this.dy = 0
		if has_moved:
			this.createSquare()
		#print(this.freeSquares)

	def move_down(this):
		has_moved = False
		for col in range(4):
			last_taken = 4
			last_grown = -1
			for row in range(3, -1, -1):
				#print(last_taken, this.grid[row][col], this.grid[last_taken][col], (row, col))
				if isinstance(this.grid[row][col], Empty):
					continue
				elif (last_taken == 4 or 
						last_grown == last_taken or
						this.grid[last_taken][col].value != this.grid[row][col].value):
					this.freeSquares.append((row, col))
					if (last_taken - 1, col) in this.freeSquares:
						this.freeSquares.remove((last_taken - 1, col))
					temp = this.grid[row][col]
					this.grid[row][col] = Empty((row, col))
					this.grid[last_taken - 1][col] = temp
					temp.position = (last_taken - 1, col)
					this.movingSquares.append({'square':temp, 'target': coordinates((last_taken - 1, col))})
					last_taken -= 1
					if last_taken != row:
						has_moved = True
				else:
					this.freeSquares.append((row, col))
					this.score += this.grid[last_taken][col].grow()
					last_grown = last_taken
					this.score_box = base_font.render(f'Score: {this.score}', False, (0, 0, 0))
					this.willFuse.append(this.grid[row][col])
					this.movingSquares.append({'square':this.grid[row][col], 'target': coordinates((last_taken, col))})
					has_moved = True
		#print(this.freeSquares)
		this.dx = 0
		this.dy = 15
		if has_moved:
			this.createSquare()
		#print(this.freeSquares)

	def move_left(this):
		has_moved = False
		for row in range(4):
			last_taken = -1
			last_grown = -1
			for col in range(4):
				#print(last_taken, this.grid[row][col], this.grid[last_taken][col], (row, col))
				if isinstance(this.grid[row][col], Empty):
					continue
				elif (last_taken == -1 or 
						last_grown == last_taken or
						this.grid[row][last_taken].value != this.grid[row][col].value):
					this.freeSquares.append((row, col))
					if (row, last_taken + 1) in this.freeSquares:
						this.freeSquares.remove((row, last_taken + 1))
					temp = this.grid[row][col]
					this.grid[row][col] = Empty((row, col))
					this.grid[row][last_taken + 1] = temp
					temp.position = (row, last_taken + 1)
					this.movingSquares.append({'square':temp, 'target': coordinates((row, last_taken + 1))})
					last_taken += 1
					if last_taken != col:
						has_moved = True
				else:
					this.freeSquares.append((row, col))
					this.score += this.grid[row][last_taken].grow()
					last_grown = last_taken
					this.score_box = base_font.render(f'Score: {this.score}', False, (0, 0, 0))
					this.willFuse.append(this.grid[row][col])
					this.movingSquares.append({'square':this.grid[row][col], 'target': coordinates((row, last_taken))})
					has_moved = True
		#print(this.freeSquares)
		this.dx = -15
		this.dy = 0
		if has_moved:
			this.createSquare()
		#print(this.freeSquares)
	
	def update(this):
		delList = []
		delSqList = []
		for sq in this.movingSquares:
			#print(sq['square'].box.left, sq['square'].box.top)
			if (sq['square'].box.left != sq['target'][0] or
				sq['square'].box.top != sq['target'][1]):
				sq['square'].box.left += this.dx
				sq['square'].box.top += this.dy
			else:
				delList.append(sq) 
				delSqList.append(sq['square']) 
			#print(sq['square'].box.left, sq['square'].box.top)
		for sq in this.willFuse:
			if sq in delSqList:
				if sq.position in this.freeSquares:
					this.grid[sq.position[0]][sq.position[1]] = Empty(sq.position)
		this.movingSquares = list(filter(lambda sq: sq not in delList, this.movingSquares))
		this.willFuse = list(filter(lambda sq: sq not in delSqList, this.willFuse))
	
	def isGameOver(this):
		if this.freeSquares:
			return False
		for i in range(1,3):
			for j in range(4):
				if 	(this.grid[i][j].value == this.grid[i-1][j].value
					or this.grid[i][j].value == this.grid[i+1][j].value
					or this.grid[j][i].value == this.grid[j][i-1].value
					or this.grid[j][i].value == this.grid[j][i+1].value):
					return False
		return True
					
	def show(this):
		display.fill(bg_color)
		display.blit(this.score_box, (25, 50))
		for row in this.grid:
			for sq in row:
				if isinstance(sq, Empty):
					sq.show()
		for row in this.grid:
			for sq in row:
				if not isinstance(sq, Empty):
					sq.show()

	

if __name__ == '__main__':

	width, height = 550, 800
	bg_color = pygame.Color(187, 173, 160)
	display = pygame.display.set_mode((width,height))
	pygame.display.set_caption('2048')

	clock = pygame.time.Clock()

	grid = Grid()
	up_pressed, down_pressed, right_pressed, left_pressed = False, False, False, False
	x, y = 0, 0

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.touch:
					x, y = event.pos
			if event.type == pygame.MOUSEBUTTONUP:
				if event.touch:
					x -= event.pos[0]
					y -= event.pos[1]
					if y >= x:
						if y >= -x:
							grid.move_up()
						else:
							grid.move_right()
					else:
						if y >= -x:
							grid.move_left()
						else:
							grid.move_down()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					up_pressed = True
				elif event.key == pygame.K_RIGHT:
					right_pressed = True
				elif event.key == pygame.K_DOWN:
					down_pressed = True
				elif event.key == pygame.K_LEFT:
					left_pressed = True
			if event.type == pygame.KEYUP:
				if up_pressed and event.key == pygame.K_UP:
					up_pressed = False
					grid.move_up()
				elif right_pressed and event.key == pygame.K_RIGHT:
					right_pressed = False
					grid.move_right()
				elif down_pressed and event.key == pygame.K_DOWN:
					down_pressed = False
					grid.move_down()
				elif left_pressed and event.key == pygame.K_LEFT:
					left_pressed = False
					grid.move_left()

		if grid.movingSquares or grid.willFuse:
			grid.update()
			grid.show()
		
		elif grid.isGameOver():
			if input("Game over! Enter y for new game") in ('y', 'Y'):
				grid = Grid()
			else:
				pygame.quit()
				exit()

		pygame.display.flip()
		clock.tick(120)

print("Boo hoo")