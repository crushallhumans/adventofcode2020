# adventofcode 2020
# crushallhumans
# puzzle 13
# 12/13/2020

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
	board_time = int(lines[0])
	min_wait = board_time
	min_wait_bus = 0
	bus_intervals = lines[1].split(',')
	bus_board_times = {}
	for ii in bus_intervals:
		if ii == 'x':
			continue
		else:
			i = int(ii)
		c = board_time
		max_step_back = board_time - (i * 3)
		if DEBUG: print ("bus",i)
		while c > max_step_back:
			if DEBUG: print ("\tc",c)
			if not c % i:
				bus_board_time = c + i
				bus_board_times[i] = bus_board_time
				if (bus_board_time - i) < min_wait:
					min_wait = bus_board_time - i
					min_wait_bus = i
				break
			c -= 1
		if i not in bus_board_times:
			raise
		if DEBUG: print(bus_board_times)
		if DEBUG: print(min_wait_bus)
		if DEBUG: print(bus_board_times[min_wait_bus])
	return min_wait_bus * (bus_board_times[min_wait_bus] - board_time)


def extended_action(param_set):
	lines = param_set.splitlines()
	board_time = int(lines[0])
	bus_intervals = lines[1].split(',')
	bus_board_time_sequence = {}
	largest = 0
	largest_idx = 0
	c = 0
	for ii in bus_intervals:
		if ii == 'x':
			continue
		else:
			i = int(ii)
		if i > largest:
			largest = i
			largest_idx = c
		c += 1
	c = 0
	for ii in bus_intervals:
		bus_board_time_sequence[i] = 0


	min_timestamp = find_min_union()

	return min_timestamp



def puzzle_text():
	print("""

""")

class testCase(unittest.TestCase):

	def setUp(self):
		self.teststring = """939
7,13,x,x,59,x,31,19"""


	def test_basic_action(self):
		self.assertEqual(
			basic_action(self.teststring),
			295
		)
	def test_extended_action(self):
		self.assertEqual(extended_action("17,x,13,19"),3417)
		self.assertEqual(extended_action("67,7,59,61"),754018)
		self.assertEqual(extended_action("67,x,7,59,61"),779210)
		self.assertEqual(extended_action("67,7,x,59,61"),1261476)
		self.assertEqual(extended_action("1789,37,47,1889"),1202161486)


if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day13.txt') as input_file:
			input_set = input_file.read()

		print(basic_action(input_set))

	print ("done");

