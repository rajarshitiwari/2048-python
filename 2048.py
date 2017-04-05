#!/usr/bin/python

# READ 1
##################################################################
# This code is written by Rajarshi Tiwari (rajarshi84@gmail.com) #
# Kindly send your query and suggestions to my email.			 #
# -Rajarshi														 #
##################################################################

# READ 2
########################################################################
# This code is tested on linux, and should run on most linux systems.  #
# You need numpy, random and curses module to run this code. In future #
# I would replace the use of array with simply a list, in which case   #
# one would not require numpy, however the modules random and curses   #
# are essential requirement.										   #
# - Rajarshi														   #
########################################################################


#from os import system
import curses
import random
import numpy
from curses.textpad import *

def shift_increase(arr):
	#SHIFT ALL ZEROS TO RIGHT
	c = 0; num = len(arr)
	i = num-1;
	while ( i > 0 ):
		if (arr[i] == 0):
			c = 0
			for j in range(i,-1,-1):
				if (arr[j] == 0):
					c += 1
				else:
					break
				#
			#
			if (c != 0):
				for j in range(i,c-1,-1):
					arr[j] = arr[j-c]
				#
				arr[0:c] = 0
			#
		#
		i -= 1
	#
	#add consecutive numbers
	c = 0
	i = num-1
	score = 0;
	while ( i >= 1 ):
		if (arr[i] == 0):
			break
		#
		if (arr[i] == arr[i-1]):
			term = arr[i] * 2
			arr[i] = term
			score += term
			for j in range(i-1,0,-1):
				arr[j] = arr[j-1]
			#
			arr[0] = 0
		#
		i -= 1
	#
	return score
#

def shift_decrease(arr):
	#shift all zeros to right
	c = 0; num = len(arr)
	i = 0
	while ( i < num - 1 ):
		if (arr[i] == 0):
			c = 0
			for j in range(i,num,1):
				if (arr[j] == 0):
					c += 1
				else:
					break
				#
			#
			if (c != 0):
				for j in range(i,num-c,1):#???
					arr[j] = arr[j+c]
				#
				arr[num-c:num] = 0
			#
		#
		i += 1
	#
	#add consecutive numbers
	c = 0
	i = 0
	score = 0;
	while ( i < num-1 ):
		if (arr[i] == 0):
			break
		#
		if (arr[i] == arr[i+1]):
			term = arr[i] * 2
			arr[i] = term
			score += term
			for j in range(i+1,num-1,1):
				arr[j] = arr[j+1]
			#
			arr[num-1] = 0
		#
		i += 1;
	#
	return score
#


def main():

	screen = curses.initscr()
	curses.cbreak()
	screen.keypad(True)
	screen.addstr(1, 2, "Press q to Exit ")
	#screen.immedok(True)
	#screen.clear()
	screen.border(0)
	
	curses.start_color()
	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
	curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

	color_arr = [2,4,8,16,32,64,128,256,512,1024,2048,4096,8192]
	
	x0=16;y0=3
	cellx = 12;celly=6
	ncell = 4
	
	curr_arr = numpy.zeros((ncell,ncell),dtype=int)
	prev_arr = numpy.zeros((ncell,ncell),dtype=int)

	r1 = random.randint(0,ncell-1)
	r2 = random.randint(0,ncell-1)

	curr_arr[r1,r2] = 2
	prev_arr[r1,r2] = 2

	for i1 in range(0,ncell):
		for i2 in range(0,ncell):
			term = curr_arr[i1][i2]
			x1=x0+i2*cellx+2
			x2=x0+(i2+1)*cellx-2
			y1=y0+i1*celly+1
			y2=y0+(i1+1)*celly-1
			cl_print = 0
			cterm = str(term)
			lnch = len(cterm)
			for i in range(0,13):
				if (term == color_arr[i]):
					if (i < 6):
						screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, str(term),curses.color_pair(i+1))
						cl_print = 1
					elif (i >= 6):
						screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, str(term),curses.color_pair(i-5)+curses.A_BOLD)
						cl_print = 1
					#
				#
				if (cl_print == 0):
					if (term == 0):
						#screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2, str(term),curses.color_pair(0))
						screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, ' ')
						#continue
					else:
						screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, str(term),curses.color_pair(0)+curses.A_BOLD)
					#
				#
			#
			#screen.addstr(y1+celly/2 -1,x1+cellx/2 -2 ,str(term))
			
			rectangle(screen, y1 ,x1 ,y2 ,x2 )
			screen.refresh()
		#
	#

	game_count = 0
	game_score = 0
	game_end = 0

	maxln = 1	
	key=''
	while key != ord('q'):
		#
		numpy.copyto(prev_arr,curr_arr)
		#
		key = screen.getch()
		#
		temp_score = 0
		if key == curses.KEY_UP:
			screen.addstr(3, 3, "UP   ")
			for i2 in range(0,ncell):
				arr1d = curr_arr[:,i2]
				temp_score = shift_decrease(arr1d)
				game_score += temp_score
			#
		elif key == curses.KEY_DOWN:
			screen.addstr(3, 3, "DOWN ")
			for i2 in range(0,ncell):
				arr1d = curr_arr[:,i2]
				temp_score = shift_increase(arr1d)
				game_score += temp_score
			#
		elif key == curses.KEY_RIGHT:
			screen.addstr(3, 3, "RIGHT")
			for i1 in range(0,ncell):
				arr1d = curr_arr[i1,:]
				temp_score = shift_increase(arr1d)
				game_score += temp_score
			#
		elif key == curses.KEY_LEFT:
			screen.addstr(3, 3, "LEFT ")
			for i1 in range(0,ncell):
				arr1d = curr_arr[i1,:]
				temp_score = shift_decrease(arr1d)
				game_score += temp_score
			#
		#
		#
		idiff = 0
		izero = 0 #(prev_arr==curr_arr).all()
		for i1 in range(0,ncell):
			for i2 in range(0,ncell):
				if (prev_arr[i1][i2] != curr_arr[i1][i2]):
					idiff +=1
				#
				if (curr_arr[i1][i2] == 0):
					izero +=1
				#
			#
		#
		if (idiff != 0):
			game_count += 1
		elif (izero > 0):
			#CAN NOT MOVE!
			continue
		else:
			#'GAME OVER'
			game_end = 1
			break;
		#
		while izero:
			r1 = random.randint(0,ncell-1)
			r2 = random.randint(0,ncell-1)
			if (curr_arr[r1][r2] == 0):
				curr_arr[r1][r2] = 2
				break
			#
		#
		for i1 in range(0,ncell):
			for i2 in range(0,ncell):
				term = curr_arr[i1][i2]
				x1=x0+i2*cellx+2
				x2=x0+(i2+1)*cellx-2
				y1=y0+i1*celly+1
				y2=y0+(i1+1)*celly-1
				screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2, (cellx)*" ")
				#screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2, str(term))
				rectangle(screen, y1 ,x1 ,y2 ,x2 )
				screen.refresh()
				cterm = str(term)
				lnch = len(cterm)
				if (maxln < lnch):
					maxln = lnch
				#
				cl_print = 0
				for i in range(0,13):
					if (term == color_arr[i]):
						if (i < 6):
							screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - maxln/2, (maxln+1)*' ')
							screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, str(term),curses.color_pair(i+1))
							cl_print = 1
						elif (i >= 6):
							screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - maxln/2, (maxln+1)*' ')
							screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, str(term),curses.color_pair(i-5)+curses.A_BOLD)
							cl_print = 1
						#
					#
					if (cl_print == 0):
						if (term == 0):
							#screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2, str(term),curses.color_pair(0))
							#screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, ' ')
							screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - maxln/2, (maxln+1)*' ')
						else:
							screen.addstr(y1+celly/2 - 1, x1+cellx/2 - 2 - lnch/2, str(term),curses.color_pair(0)+curses.A_BOLD)
						#
					#
				screen.refresh()
			#
		#
		screen.addstr(4,3,"count = "+str(game_count))
		screen.addstr(5,3,"score = "+str(game_score))
		screen.refresh()
	#
	curses.endwin()
	print "number of moves = ",game_count
	print "game score      = ",game_score
	print "thank you for playing!"
	
#

if __name__ == '__main__':
	main()
