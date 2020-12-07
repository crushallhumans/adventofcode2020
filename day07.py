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

