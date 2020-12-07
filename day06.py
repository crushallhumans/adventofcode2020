# adventofcode 2020
# crushallhumans
# puzzle 6
# 12/6/2020

import sys
import math
import unittest

def basic_action(param_set):
	# parse groups
	lines = param_set.splitlines()
	groups = []
	group = {}

	for i in lines:
		if i == "":
			groups.append(len(group.keys()))
			group = {}
			continue
		for j in i:
			group[j] = True
#		for j in range(97,123):
#			c = chr(j)
	groups.append(len(group.keys()))

	return (groups,sum(groups))

def additional_action(param_set):
	# parse groups
	lines = param_set.splitlines()
	groups = []
	group = {}

	group_size = 0
	for i in lines:
		if i == "":
			groups.append(check_group(group, group_size))
			group = {}
			group_size = 0
			continue
		for j in i:
			if j not in group:
				group[j] = 0
			group[j] += 1
		group_size += 1

	groups.append(check_group(group, group_size))

	return (groups,sum(groups))

def check_group(group, group_size):
	size = 0
	for i in group.keys():
		if group[i] == group_size:
			size += 1
	return size


def puzzle_text():
	print("""
--- Day 6: Custom Customs ---
As your flight approaches the regional airport where you'll switch to a much larger plane, customs declaration forms are distributed to the passengers.

The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.

However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help. For each of the people in their group, you write down the questions for which they answer "yes", one per line. For example:

abcx
abcy
abcz
In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)

Another group asks for your help, then another, and eventually you've collected answers from every group on the plane (your puzzle input). Each group's answers are separated by a blank line, and within each group, each person's answers are on a single line. For example:

abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:

The first group contains one person who answered "yes" to 3 questions: a, b, and c.
The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
The last group contains one person who answered "yes" to only 1 question, b.
In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.

For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?

--- Part Two ---
As you finish the last group's customs declaration, you notice that you misread one word in the instructions:

You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!

Using the same example as above:

abc

a
b
c

ab
ac

a
a
a
a

b
This list represents answers from five groups:

In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
In the second group, there is no question to which everyone answered "yes".
In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
In the fourth group, everyone answered yes to only 1 question, a.
In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.

For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
""")

class testCase(unittest.TestCase):

	def setUp(self):
		self.teststring = """abc

a
b
c

ab
ac

a
a
a
a

b"""


	def test_basic_action(self):
		self.assertEqual(
			basic_action(self.teststring),
			([3,3,3,1,1],11)
		)

	def test_additional_action(self):
		self.assertEqual(
			additional_action(self.teststring),
			([3,0,1,1,1],6)
		)


if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day06.txt') as input_file:
		    input_set = input_file.read()

		print(basic_action(input_set))
		print(additional_action(input_set))

	print ("done");

