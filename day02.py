# adventofcode 2020
# crushallhumans
# puzzle 2
# 12/2/2020

import re
import sys
import math
import unittest

def basic_action(param_set):
	# parse policy
	p = re.compile('(\d+)-(\d+) (\w): (\w+)')
	m = p.match(param_set)
	if not m.groups():
		return False
	policy_map = {}
	policy_map[m.group(3)] = {
		'floor': int(m.group(1)),
		'limit': int(m.group(2)),
		'counter': 0
	}

	# validate password
	password = m.group(4)
	for i in password:
		for k in policy_map:
			if i == k:
				policy_map[k]['counter'] += 1
			if policy_map[k]['counter'] > policy_map[k]['limit']:
				return False

	for k in policy_map:
		if policy_map[k]['counter'] < policy_map[k]['floor']:
			return False

	return True


def additional_action(param_set):
	# parse policy
	p = re.compile('(\d+)-(\d+) (\w): (\w+)')
	m = p.match(param_set)
	if not m.groups():
		return False
	policy_map = {}
	policy_map[m.group(3)] = {
		'pos1': int(m.group(1)),
		'pos2': int(m.group(2)),
		'counter': 0
	}

	# validate password
	password = m.group(4)
	c = 1
	for i in password:		
		for k in policy_map:
			if i == k and (c == policy_map[k]['pos1'] or c == policy_map[k]['pos2']):
				policy_map[k]['counter'] += 1
			if policy_map[k]['counter'] > 1:
				return False
		c += 1

	for k in policy_map:
		if policy_map[k]['counter'] < 1:
			return False

	return True


def puzzle_text():
	print("""
--- Day 2: Password Philosophy ---
Your flight departs in a few days from the coastal airport; the easiest way down to the coast from here is via toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day. "Something's wrong with our computers; we can't log in!" You ask if you can take a look.

Their password database seems to be a little corrupted: some of the passwords wouldn't have been allowed by the Official Toboggan Corporate Policy that was in effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
Each line gives the password policy and then the password. The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.

How many passwords are valid according to their policies?

--- Part Two ---
While it appears you validated the passwords correctly, they don't seem to be what the Official Toboggan Corporate Authentication System is expecting.

The shopkeeper suddenly realizes that he just accidentally explained the password policy rules from his old job at the sled rental place down the street! The Official Toboggan Corporate Policy actually works a little differently.

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy enforcement.

Given the same example list from above:

1-3 a: abcde is valid: position 1 contains a and position 3 does not.
1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.
How many passwords are valid according to the new interpretation of the policies?
""")

class testCase(unittest.TestCase):
	def test_basic_action(self):
		self.assertEqual(
			basic_action("1-3 a: abcde"),
			True
		)
		self.assertEqual(
			basic_action("1-3 b: cdefg"),
			False
		)
		self.assertEqual(
			basic_action("2-9 c: ccccccccc"),
			True
		)

	def test_additional_action(self):
		self.assertEqual(
			additional_action("1-3 a: abcde"),
			True
		)
		self.assertEqual(
			additional_action("1-3 b: cdefg"),
			False
		)
		self.assertEqual(
			additional_action("2-9 c: ccccccccc"),
			False
		)

if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day02.txt') as input_file:
		    input_set = [input_line.strip() for input_line in input_file]

		trues_basic = 0
		trues_addl = 0
		for i in input_set:
			if (basic_action(i)):
				trues_basic += 1
			if (additional_action(i)):
				trues_addl += 1

		print(trues_basic)
		print(trues_addl)

	print ("done");

