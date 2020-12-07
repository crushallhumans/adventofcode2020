# adventofcode 2020
# crushallhumans
# puzzle 7
# 12/7/2020

import re
import sys
import math
import unittest

def basic_action(param_set, sample, counts = False):
	# parse rules
	lines = param_set.splitlines()
	container_rules = {}
	parentage_rules = {}
	all_colors = {}
	for ii in lines:
		i = ii[:-1]
		#print(i)
		kv = i.split(' bags contain ')
		container = 	kv[0]
		all_children = 	kv[1]
		if not container in container_rules:
			container_rules[container] = []
		if not 'no other bags' in all_children:
			all_colors[container] = True
			for j in all_children.split(', '):
				pp = re.compile('(\d+) (\w+ \w+) bags?')
				mm = pp.match(j)
				if not mm or not mm.groups() or not mm.groups(1):
					print(j)
				quantity = mm.group(1)
				color = mm.group(2)
				all_colors[color] = True
				# rule: lists of required children
				container_rules[container].append((color,quantity))
				# rule: lists of possible parents
				if not color in parentage_rules:
					parentage_rules[color] = []
				parentage_rules[color].append(container)

#	print(container_rules)
#	print(parentage_rules)

	global check_dict
	global count_dict
	check_dict = {}
	check_rule(parentage_rules, sample)
	count = count_containers(container_rules,sample)

	if counts:
		return count
	else:
		return (len(check_dict))

def check_rule(parentage_rules, sample):
	# print ("checking ", sample)
	if not sample in parentage_rules:
		# print ("no rule for ", sample)
		return True
	else:
		for i in parentage_rules[sample]:
			check_dict[i] = True
			check_rule(parentage_rules, i)

def count_containers(container_rules, sample, n = 0):
	if not len(container_rules[sample]):
		return 1

	total = 1
#	print (" "*n+sample)
	for i in container_rules[sample]:
#		print (" "*n+str(i))
		total += int(i[1]) * count_containers(container_rules, i[0], n + 1)

	if n == 0:
		total -= 1
	return total



def puzzle_text():
	print("""
--- Day 7: Handy Haversacks ---
You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. Apparently, nobody responsible for these regulations considered how long they would take to enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)

--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
""")

class testCase(unittest.TestCase):

	def setUp(self):
		self.teststring = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
		self.teststring2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

	def test_basic_action(self):
		self.assertEqual(
			basic_action(self.teststring, 'shiny gold'),
			4
		)

	def test_additional_action(self):
		self.assertEqual(
			basic_action(self.teststring, 'shiny gold', True),
			32
		)
		self.assertEqual(
			basic_action(self.teststring2, 'shiny gold', True),
			126
		)


if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day07.txt') as input_file:
		    input_set = input_file.read()

		print(basic_action(input_set, 'shiny gold'))
		print(basic_action(input_set, 'shiny gold', True))

	print ("done");

