# adventofcode 2020
# crushallhumans
# puzzle 10
# 12/10/2020

import re
import copy
import sys
import math
import itertools
import unittest
from functools import cache
import hashlib

DEBUG = False

def basic_action(param_set):
	# parse field
	lines = param_set.splitlines()
	location = {
		'x': 0,
		'y': 0
	}
	dir_map_basic = {
		'N': ('y', -1, 0),
		'E': ('x', 1, 90),
		'S': ('y', 1, 180),
		'W': ('x', -1, 270),
		'R': ('d', 1),
		'L': ('d', -1),
		'F': ('f')
	}
	dir_map = {}
	for k in dir_map_basic:
		dir_map[k] = dir_map_basic[k]
		v = dir_map_basic[k]
		if len(v) == 3:
			dir_map[v[2]] = dir_map_basic[k]

	facing = dir_map['E'][2] #90
	for i in lines:
		p = re.compile('(\w)(\d+)')
		m = p.match(i)
		if not m or not m.groups():
			return False
		instruction = dir_map[m.group(1)]
		if instruction[0] == 'f':
			instruction = dir_map[facing]
		param = int(m.group(2))
		if instruction[0] == 'd':
			j = 0
			while j < param:
				facing += instruction[1]
				if facing < 0:
					facing = 360 + instruction[1]
				elif facing == 360:
					facing = 0
				j += 1
			if DEBUG: print (i, facing)
		else:
			location[instruction[0]] += instruction[1] * param
		if DEBUG: print (location)

	x = abs(location['x']) + abs(location['y'])
	return (x, location)


def extended_action(param_set):
	# parse field
	lines = param_set.splitlines()
	location = {
		'x': 0,
		'y': 0
	}
	waypoint = {
		'x': 10,
		'y': 1
	}
	dir_map = {
		'N': ('y', 1),
		'E': ('x', 1),
		'S': ('y', -1),
		'W': ('x', -1),
		'R': ('d', -1),
		'L': ('d', 1),
		'F': ('f')
	}

	if DEBUG: print ("")
	for i in lines:
		p = re.compile('(\w)(\d+)')
		m = p.match(i)
		if not m or not m.groups():
			return False
		if DEBUG: print (i)
		instruction = dir_map[m.group(1)]
		param = int(m.group(2))
		if instruction[0] == 'd':
			px = waypoint['x']
			py = waypoint['y']

			# attempt 3
			rad = ((param * instruction[1])/90) * (math.pi/2)
			waypoint['x'] = round(px * math.cos(rad) - py * math.sin(rad))
			waypoint['y'] = round(px * math.sin(rad) + py * math.cos(rad))

			# attempt 1
			#p'x = cos(theta) * (px-ox) - sin(theta) * (py-oy) + ox
			#p'y = sin(theta) * (px-ox) + cos(theta) * (py-oy) + oy
			#waypoint['x'] = round(math.cos(math.radians(param * instruction[1])) * (px) - math.sin(math.radians(param * instruction[1])) * (py))
			#waypoint['y'] = round(math.sin(math.radians(param * instruction[1])) * (px) - math.cos(math.radians(param * instruction[1])) * (py))

			# attempt 2
			# rotation = param
			# if m.group(1) == 'L':
			# 	rotation = (0 - param) % 360
			# print (rotation)
			# if rotation == 90:
			# 	waypoint['x'] = waypoint['y']
			# 	waypoint['y'] = 0 - px
			# elif rotation == 180:
			# 	waypoint['x'] = 0 - waypoint['x']
			# 	waypoint['y'] = 0 - waypoint['y']
			# elif rotation == 270:
			# 	waypoint['x'] = waypoint['y']
			# 	waypoint['y'] = px

			if DEBUG: print (i, waypoint)
		elif instruction[0] == 'f':
			location['x'] += waypoint['x'] * param
			location['y'] += waypoint['y'] * param
		else:
			waypoint[instruction[0]] += instruction[1] * param

		if DEBUG: print (location, waypoint)

	x = abs(location['x']) + abs(location['y'])
	return (x, location)



def puzzle_text():
	print("""
--- Day 12: Rain Risk ---
Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!

Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.

The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

Action N means to move north by the given value.
Action S means to move south by the given value.
Action E means to move east by the given value.
Action W means to move west by the given value.
Action L means to turn left the given number of degrees.
Action R means to turn right the given number of degrees.
Action F means to move forward by the given value in the direction the ship is currently facing.
The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)

For example:

F10
N3
F7
R90
F11
These instructions would be handled as follows:

F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
N3 would move the ship 3 units north to east 10, north 3.
F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
F11 would move the ship 11 units south to east 17, south 8.
At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?

--- Part Two ---
Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.

Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.
The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

For example, using the same instructions as above:

F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?
""")

class testCase(unittest.TestCase):

	def setUp(self):
		self.teststring = """F10
N3
F7
R90
F11"""


	def test_basic_action(self):
		self.assertEqual(
			basic_action(self.teststring)[0],
			25
		)
	def test_extended_action(self):
		self.assertEqual(
			extended_action(self.teststring)[0],
			286
		)



if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day12.txt') as input_file:
			input_set = input_file.read()

		#print(basic_action(input_set)[0])
		print(extended_action(input_set)[0])

	print ("done");

