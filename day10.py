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


DEBUG = False

def basic_action(param_set):
	# parse rules
	jolts = [int(x) for x in param_set.splitlines()]
	jolts.sort()
	effective_joltage = 0
	diff_map = {}
	optional_tips = []
	c = 0
	for i in jolts:
		diff = i - effective_joltage
		if (diff > 3):
			return False
		effective_joltage = i
		if diff < 3:
			optional_tips.append(i)
		ds = str(diff)
		#print(i,ds)
		if not ds in diff_map:
			diff_map[ds] = 0
		diff_map[ds] += 1
		effective_joltage = i
		c += 1

	possible_combos = test_attachments(jolts)

	diff_map["3"] += 1

	return (diff_map, (diff_map["1"] * diff_map["3"]), possible_combos)

def test_attachments(jolts):
    top = max(jolts)

    @cache
    def _attach(starting_at):
        if starting_at == top:
            return 1
        internal_recursion_results = []
        for i in range(1,4):
        	starting_at_internal = starting_at + i
        	if starting_at_internal in jolts:
        		internal_recursion_results.append(_attach(starting_at_internal))
        return sum(internal_recursion_results)

    return _attach(0)


def puzzle_text():
	print("""
""")

class testCase(unittest.TestCase):

	def setUp(self):
		self.teststring = """16
10
15
5
1
11
7
19
6
12
4"""

		self.teststring2 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

	def test_basic_action(self):
		self.assertEqual(
			basic_action(self.teststring)[0],
			{'3': 5, '1': 7}
		)
		self.assertEqual(
			basic_action(self.teststring2)[0],
			{'3': 10, '1': 22}
		)

		self.assertEqual(
			basic_action(self.teststring)[2],
			8
		)
		self.assertEqual(
			basic_action(self.teststring2)[2],
			19208
		)


if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day10.txt') as input_file:
		    input_set = input_file.read()

		print(basic_action(input_set))

	print ("done");

