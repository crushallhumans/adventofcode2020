# adventofcode 2020
# crushallhumans
# puzzle 4
# 12/4/2020

import re
import sys
import math
import numpy
import unittest

def basic_action(param_set):
	# parse seat
	ROW_MAX = 127
	COL_MAX = 7
	# print(param_set)
	operating_set = (0,ROW_MAX)
	div_values = ('F','B')

	row = -1
	for i in list(param_set):
		# print (i)
		if i not in div_values:
			row = operating_set[0]
			operating_set = (0,COL_MAX)
			div_values = ('L','R')
		# print ("before: ", operating_set)
		diff = math.floor((operating_set[1]-operating_set[0])/2)+operating_set[0]
		halves = [
			operating_set[0],
			diff,
			diff + 1,
			operating_set[1]
		]
		# print (halves)
		# upper
		if i == div_values[0]:
			operating_set = (halves[0],halves[1])
		#lower
		elif i == div_values[1]:
			operating_set = (halves[2],halves[3])
		else:
			# print ("FAIL")
			return False
		# print ("afterr: ", operating_set)
	col = operating_set[0]
	return (row, col, (row * 8) + col)

def puzzle_text():
	print("""
--- Day 5: Binary Boarding ---
You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.

You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input); perhaps you can find your seat through process of elimination.

Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

Start by considering the whole range, rows 0 through 127.
F means to take the lower half, keeping rows 0 through 63.
B means to take the upper half, keeping rows 32 through 63.
F means to take the lower half, keeping rows 32 through 47.
B means to take the upper half, keeping rows 40 through 47.
B keeps rows 44 through 47.
F keeps rows 44 through 45.
The final F keeps the lower of the two, row 44.
The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

Start by considering the whole range, columns 0 through 7.
R means to take the upper half, keeping columns 4 through 7.
L means to take the lower half, keeping columns 4 through 5.
The final R keeps the upper of the two, column 5.
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.

Here are some other boarding passes:

BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.
As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?

--- Part Two ---
Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?
""")

class testCase(unittest.TestCase):
	def test_basic_action(self):
		self.assertEqual(basic_action(
			"FBFBBFFRLR"),
			(44,5,357)
		)
		self.assertEqual(basic_action(
			"BFFFBBFRRR"),
			(70,7,567)
		)
		self.assertEqual(basic_action(
			"FFFBBBFRRR"),
			(14,7,119)
		)
		self.assertEqual(basic_action(
			"BBFFBBFRLL"),
			(102,4,820)
		)

if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day05.txt') as input_file:
		    input_set = input_file.read().splitlines()

		highest_seat_id = 0
		matrix = {}
		for i in input_set:
			x = basic_action(i)
			if not x[0] in matrix:
				matrix[x[0]] = {}
			matrix[x[0]][x[1]] = x
			if x[2] > highest_seat_id:
				highest_seat_id = x[2]

		# cheat, draw a seat map, and find missing seat visually
		for i in range(0,127):
			print (i, end=' ')
			for j in range(0,7):
				if not i in matrix or not j in matrix[i]:
					print ('X', end='')
				else:
					print ('.', end='')
			print ("")

		print (highest_seat_id)
		# calculate the missing seat ID = row * 8 + col
		# hahaha

	print ("done");

