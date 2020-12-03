# adventofcode 2020
# crushallhumans
# puzzle 3
# 12/2/2020

import re
import sys
import math
import numpy
import unittest

def parse_map(param_set):
	# parse map
	lines = param_set.splitlines()
	matrix = []
	for i in lines:
		line = []
		for j in i:
			if (j == '.'):
				line.append(False)
			elif (j == '#'):
				line.append(True)
		matrix.append(line)

	# multiply matrix
	MULTIPLICATION_FACTOR = math.ceil(len(matrix) / 2) + 1
	multiplied_matrix = []
	for i in matrix:
		c = 0
		newline = []
		while c < MULTIPLICATION_FACTOR:
			for j in i:
				newline.append(j)
			c += 1	
		multiplied_matrix.append(newline)
	matrix = multiplied_matrix

	return matrix

def basic_action(param_set,down,right):
	matrix = parse_map(param_set)

	# count trees via slope
	x = 0
	y = 0
	trees = 0
	#print (len(matrix))
	while y < len(matrix)-down:
		x += right
		y += down
		#print (x,y)
		#print (len(matrix[y]))
		if matrix[y][x]:
			trees += 1

	#print("basic trees! ", trees, down, right)
	return trees


def additional_action(param_set, slopes):
	tree_set = []
	for i in slopes:
		#print ("addl: ", i[1],i[0])
		tree_set.append(basic_action(param_set,i[1],i[0]))
		#print (tree_set)
	return numpy.prod(tree_set)


def puzzle_text():
	print("""
--- Day 3: Toboggan Trajectory ---
With the toboggan login problems resolved, you set off toward the airport. While travel by toboggan might be easy, it's certainly not safe: there's very minimal steering and the area is covered in trees. You'll need to see which angles will take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer coordinates in a grid. You make a map (your puzzle input) of the open squares (.) and trees (#) you can see. For example:

..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
These aren't the only trees, though; due to something you read about once involving arboreal genetics and biome stability, the same pattern repeats to the right many times:

..##.........##.........##.........##.........##.........##.......  --->
#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........#.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...##....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers); start by counting all the trees you would encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with O where there was an open square and X where there was a tree:

..##.........##.........##.........##.........##.........##.......  --->
#..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
.#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
.#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
.#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
.#........#.#........X.#........#.#........#.#........#.#........#
#.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
#...##....##...##....##...#X....##...##....##...##....##...##....#
.#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
In this example, traversing the map using this slope would cause you to encounter 7 trees.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?

--- Part Two ---
Time to check the rest of the slopes - you need to minimize the probability of a sudden arboreal stop, after all.

Determine the number of trees you would encounter if, for each of the following slopes, you start at the top-left corner and traverse the map all the way to the bottom:

Right 1, down 1.
Right 3, down 1. (This is the slope you already checked.)
Right 5, down 1.
Right 7, down 1.
Right 1, down 2.
In the above example, these slopes would find 2, 7, 3, 4, and 2 tree(s) respectively; multiplied together, these produce the answer 336.

What do you get if you multiply together the number of trees encountered on each of the listed slopes?
""")

class testCase(unittest.TestCase):
	def test_basic_action(self):
		self.assertEqual(
			basic_action(
"""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
			,1,3),
			7
		)

	def test_additional_action(self):
		self.assertEqual(
			additional_action(
"""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
			,[(1,1),(3,1),(5,1),(7,1),(1,2)]),
			336
		)

if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day03.txt') as input_file:
		    input_set = input_file.read()

		print(basic_action(input_set,1,3))
		print(additional_action(input_set,[(1,1),(3,1),(5,1),(7,1),(1,2)]))

	print ("done");

