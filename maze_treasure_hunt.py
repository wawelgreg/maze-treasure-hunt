#!/usr/bin/python
import logging as log
import curses
import time
import random
import copy
import math

FRAME_SLEEP = 0.01 # how long a frame should last
WIDTH_C = 60 # Centered view width
HEIGHT_C = 30 # Centered view height
WIDTH = 1000 # Uncentered view width
HEIGHT = 1000 # Uncentered view height
CENTERED = True
WALL = '\xe2'
TAIL = '='
TREASURE = 'T'

# Generator
MIN_L = 2 #20
MAX_L = 2 #30i
MIN_N = 50000 #200
MAX_N = 50000 #300
GEN_ROWS = 300 #100
GEN_COLS = 300 #100


log.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',level=log.DEBUG, filename='mth.log', datefmt='%Y-%m-%dT%H:%M:%S%z')

log.info("----------RUNNING CLASS----------")

stdscr = curses.initscr()
pad = curses.newpad(1000,1000)	

def generator(rows_l, cols_l, wall):
	maze = []
	stack = []
	if rows_l % 2 == 0:
		rows_l += 1
	if cols_l % 2 == 0:
		cols_l += 1
	
	# Fill maze with walls
	for roww in range(rows_l):
		maze.append([wall for coll in range(cols_l)])

	r, c = 1,1
	stack.append((r,c))
	while len(stack) > 0:
		
		r,c = stack.pop()
		maze[r][c] = ' '

		look = [(-2,0), (0,2), (2,0), (0,-2)]
		random.shuffle(look)
			
		for dr, dc in look:
			nr, nc = r+dr, c+dc
			if 0<=nr<rows_l and 0<=nc<cols_l and maze[nr][nc] == WALL:
				stack.append((r,c))
				maze[r+(dr/2)][c+(dc/2)] = ' '
				stack.append((nr,nc))
				break

	trea_r, trea_c = -1, -2 # Bottom right end
	maze[trea_r][trea_c] = TREASURE
	maze[0][1] = 'S' # Top left start

	return maze, trea_r, trea_c
	
log.info("Generating maze.")
matrix, trea_r, trea_c = generator(HEIGHT, WIDTH, WALL)


def lookup_matrix_safe(r,c):
	if not (0<=r<len(matrix) and 0<=c<len(matrix[0])):
		return '*'
	return matrix[r][c]


def draw(pad):	
	for ri, crow in enumerate(matrix):
		for ci, ccol in enumerate(crow):
			pad.addch(ri,ci, matrix[ri][ci])


def draw_centered(pad, coord_r, coord_c, h, w):	
	for rprint in range(1,h+1):
		for cprint in range(0,w):
			frp = coord_r-(h//2)+rprint
			fcp = coord_c-(w//2)+cprint
			pad.addch(rprint,cprint, lookup_matrix_safe(frp, fcp))
	
	# trea_r, trea_c

	# Calculate distance: (r2-r1)/(x2-x1)

	#distance = math.dist([coor_r, trea_r], [coord_c, trea_c])
	p1 = (coord_r, coord_c)
	p2 = (coord_c, trea_c)
	distance = math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

	pad.addstr(0,0, "Distance to {}: {}".format(TREASURE, distance))


def find_start(m):
	for ri, row in enumerate(m):
		for ci, col in enumerate(row):
			if m[ri][ci] == 'S':
				log.debug("Found S at %r,%c", ri, ci)
				log.debug("Returning %r from find_start", tuple([ri, ci]))
				t = tuple([ri, ci])
				return t
	return tuple([0,0])


look = [(-1,0), (0,-1), (0,1), (1,0)]
def traverse(m, r, c, l):
	#Stack
	stack = []
	draw_row = r
	draw_col = c	

	# Local state
	row = r
	col = c
	level = l
	prefix = "level%d" %(level)
	shuffled_look = random.sample(look, len(look))
	#shuffled_look = random.shuffle(copy.copy(look))
	#shuffled_look = list(look)
	look_idx = 0
	
	while True:
		time.sleep(FRAME_SLEEP)
		m[row][col] = 'o'

		# Draw shit
		if draw_col > col:
			draw_col -= 1
		elif draw_col < col:
			draw_col += 1
		if draw_row > row:
			draw_row -= 1
		elif draw_row < row:
			draw_row += 1	
		
		pad.erase()
			
		# Draw centered or not		
		if CENTERED:
			draw_centered(pad, draw_row, draw_col, HEIGHT_C, WIDTH_C)
		else:
			draw(pad)
		
		if CENTERED:
			pad.refresh(0,0, 0,0, curses.LINES-1,curses.COLS-1)
		else:
			pad.refresh(0,0, 0,0, curses.LINES-1,curses.COLS-1)
		log.debug("%s At r:%r c:%r", prefix, row, col)
		matrix[row][col] = TAIL
		while look_idx < len(shuffled_look):
			time.sleep(FRAME_SLEEP)
			sr, sc = shuffled_look[look_idx]
			look_idx += 1
			log.debug("%s Checking %r, %r", prefix, (row+sr), (col+sc))

			if not (0<=(row+sr)<len(matrix) and 0<=(col+sc)<len(matrix[0])):
				log.debug("%s B at r:%r c:%r", prefix, (row+sr), (col+sc))
				continue

			# if wall - gtfo
			if matrix[row+sr][col+sc] == WALL:
				log.debug("%s %s at r:%r c:%r", prefix, WALL, (row+sr), (col+sc))
				continue
			
			if matrix[row+sr][col+sc] == TAIL:
				log.debug("%s %s at r:%r c:%r", prefix, TAIL, (row+sr), (col+sc))
				continue

			if matrix[row+sr][col+sc] == 'T':
				log.debug("%s Found T! at r:%r c:%r", prefix, row, col)
				return [col, row]
			
					
			log.debug("%s %r at r:%r, c:%r", prefix, ' ', (row+sr), (col+sc))
			
			# "recursive" search from sr, sc further (New local state)
			#row = row+sr
			#col = col+sc
			#level = level+1
			p = "level%d" %(level)
			#shuffled_look = list(look)
			#look_idx = 0
			#shuffled_look = random.shuffle(list(look))	
			# push goes here
			
			log.debug("Pushing to stack len:%r", len(stack))
			stack.append((row+sr, col+sc, level+1, p, random.sample(look, len(look)), 0))
			continue
			#res = traverse(m, row+sr, col+sc, level+1)
			#if res is not None:
				#return res
		# if stack empty - return None, we did not find shit
		if len(stack) == 0:
			return None		

		# pop goes here
		log.debug("Popping from stack len:%r", len(stack))
		row, col, level, prefix, shuffled_look, look_idx = stack.pop()

	# should never reach here I think
	
	return None



def func(scr):
	t = find_start(matrix)
	tr, tc = t
	r = traverse(matrix, tr, tc, 1)
	log.info("Found: %r", r)
	time.sleep(10)

if __name__ == '__main__':
	log.info("Starting new program.")
	curses.wrapper(func)
