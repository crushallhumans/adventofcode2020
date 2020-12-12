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

def basic_action(param_set, density = 4, extend = False):
	# parse field
	lines = param_set.splitlines()
	matrix = parse_matrix(lines)

	sha256 = hashlib.sha256()
	sha256.update(str(matrix).encode())
	state_sha = sha256.hexdigest()

	if DEBUG: print(assess_matrix(matrix)[1])
	if DEBUG: print(state_sha)

	field_shas = []
	c = 0
	while state_sha not in field_shas:
		field_shas.append(state_sha)
		matrix = evolve_field(matrix, density, extend)
		sha256 = hashlib.sha256()
		sha256.update(str(matrix).encode())
		state_sha = sha256.hexdigest()
		if DEBUG: print(assess_matrix(matrix)[1])
		if DEBUG: print(state_sha)
		if DEBUG: print("\n")

		c += 1

	x = assess_matrix(matrix)
	if DEBUG: print (x)
	return (x)



def evolve_field(matrix, density = 4, extend = False):

	# push into new matrix
	# foreach not None
		# get Occupied around in old matrix
		# (get Occupied around):
			# for row n and +/- 1 if exists
				# cols n and and +/- 1 if exists
					# if r[c] == True: Occupied++
		# if False and Not Occupied
			# push true
		# if True and Occupied >= 4
			# push false

	new_matrix = []
	c = 0
	for ii in range(0,len(matrix)):
		i = matrix[ii]
		row = []
		d = 0
		for jj in range(0,len(i)):
			j = i[jj]
			if j == None:
				row.append(None)
			else:
				occupied = get_occupied_around(d, c, matrix, extend)

				if j:
					if occupied >= density:
						row.append(False)
					else:
						row.append(True)
				elif not j:
					if occupied == 0:
						row.append(True)
					else:
						row.append(False)
			d += 1
		c += 1
		new_matrix.append(row)

	return new_matrix

def get_occupied_around(x, y, matrix, extend = False):
	# for row n and +/- 1 if exists
		# cols n and and +/- 1 if exists
			# if r[c] == True: Occupied++

	occupied_around = 0
	for i in range(-1,2):
		yy = y+i

		if yy >= 0 and yy < len(matrix):
			for j in range(-1,2):
				xx = x+j

				if xx >= 0 and xx < len(matrix[yy]) and not (xx == x and yy == y):
					if DEBUG: print("primary check " + str(xx) + "," + str(yy))

					if matrix[yy][xx] == True:
						occupied_around += 1
					elif extend and (matrix[yy][xx] == None):
						# extend along i and j range lines until boundary or seat encountered
						if DEBUG: print("extending " + str(xx) + "," + str(yy) + " along x,y steps: ", j, i)
						found = False
						xxx = xx
						yyy = yy
						while not found:
							xxx = xxx+j
							yyy = yyy+i
							if not (
									(yyy >= 0 and yyy < len(matrix)) and
									(xxx >= 0 and xxx < len(matrix[yyy]))
							):
								break
							if DEBUG: print("\t checking " + str(xxx) + "," + str(yyy))
							if matrix[yyy][xxx] != None:
								if DEBUG: print("\t found ", matrix[yyy][xxx])
								if matrix[yyy][xxx] == True:
									occupied_around += 1
								found = True


	return occupied_around

def test_visibility(param_set, x, y, extend = True):
	# parse field
	lines = param_set.splitlines()
	matrix = parse_matrix(lines)
	if DEBUG: print(assess_matrix(matrix)[1])

	return get_occupied_around(x, y, matrix, extend)

def parse_matrix(lines):
	matrix = []
	for i in lines:
		row = []
		for j in i:
			m = None
			if j == 'L':
				m = False
			elif j == '#':
				m = True
			row.append(m)
		matrix.append(row)
	return matrix

def assess_matrix(m):
	printable = ''
	hashable = ''
	num_occupied = 0
	c = 0
	line = '  '
	for i in m:
		line += str(c)
		c += 1
	printable += line + "\n"
	c = 0
	for i in m:
		line = str(c) + ' '
		d = 0
		for j in i:
			if j == None:
				line += '.'
			elif j == True:
				line += '#'
				num_occupied += 1
			elif j == False:
				line += 'L'
			d += 1
		printable += line + "\n"
		hashable += line
		c += 1

	return (num_occupied, printable, hashable)


def puzzle_text():
	print("""
--- Day 11: Seating System ---
Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
Otherwise, the seat's state does not change.
Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
After a second round, the seats with four or more occupied adjacent seats become empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##
#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##
#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?


--- Part Two ---
As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:

.............
.L.L.#.#.#.#.
.............
The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.

Given the same starting layout as above, these new rules cause the seating area to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#
#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#
Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?

""")

class testCase(unittest.TestCase):

	def setUp(self):
		self.teststring = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

		self.teststring2 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

		self.visibility_test_1 = """.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#....."""
		self.visibility_test_2 = """.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##."""


	def test_basic_action(self):
		self.assertEqual(
			basic_action(self.teststring)[0],
			37
		)
	def test_visibility(self):
		self.assertEqual(
			test_visibility(self.visibility_test_1, 3, 4, True),
			8
		)
		self.assertEqual(
			test_visibility(self.visibility_test_2, 3, 3, True),
			0
		)
	def test_extended_action(self):
		self.assertEqual(
			basic_action(self.teststring, 5, True)[0],
			26
		)


if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day11.txt') as input_file:
		    input_set = input_file.read()

		print(basic_action(input_set)[0])
		print(basic_action(input_set, 5, True)[0])

	print ("done");

