# adventofcode 2020
# crushallhumans
# puzzle 8
# 12/8/2020

import re
import copy
import sys
import math
import unittest

DEBUG = False

def basic_action(param_set, test = False):
	# parse rules
	lines = param_set.splitlines()
	instruction_set = []
	for i in lines:
		instruction_set.append(process_instruction_string(i))

	if test:
		return test_program(instruction_set)
	else:
		return execute_program(instruction_set)


def process_instruction_string(instruction):
	i = instruction.split(' ')
	commander = i[0]
	parameter = int(i[1])
	return ((commander,parameter))

def execute_program(instruction_set):
	program_cur = 0
	accumulator = 0
	step = 0
	command_counter = {}
	terminated = 0
	while not terminated:
		if program_cur == (len(instruction_set)):
			if DEBUG: print ("Terminated, " + str(program_cur) + " == " + str(len(instruction_set)))
			terminated = 1
			continue

		commander = instruction_set[program_cur][0]
		parameter = instruction_set[program_cur][1]
		counter_key = commander+str(program_cur)
		if not counter_key in command_counter:
			command_counter[counter_key] = 0

		command_counter[counter_key] += 1

		if DEBUG: print(step, program_cur, instruction_set[program_cur], accumulator)

		if command_counter[counter_key] > 1:
			if DEBUG: print ("Looped!")
			terminated = 2
			continue

		(program_cur_incr, accumulator_incr) = process_instruction(commander, parameter, instruction_set, program_cur)
		program_cur += program_cur_incr
		accumulator	+= accumulator_incr

		step += 1

	return (accumulator, terminated)

def test_program(instruction_set):
	result = 2
	mod_counter = 0
	while result == 2:
		inner_set = copy.deepcopy(instruction_set)
		mod = False
		while not mod:
			if 		inner_set[mod_counter][0] == 'nop':
				inner_set[mod_counter] = ('jmp', inner_set[mod_counter][1])
				mod = True
			elif 	inner_set[mod_counter][0] == 'jmp':
				inner_set[mod_counter] = ('nop', inner_set[mod_counter][1])
				mod = True
			mod_counter += 1

		(acc, result) = execute_program(inner_set)

	return (acc, result, mod_counter)

def process_instruction(commander, parameter, program, cursor):
	if 		(commander == 'nop'):
		return(1,0)
	elif	(commander == 'jmp'):
		return(parameter,0)
		# jump_state = cursor + parameter
		# jump_instr = program[jump_state]
		# return process_instruction(jump_instr[0], jump_instr[1], program, jump_state)
	elif	(commander == 'acc'):
		return(1,parameter)



def puzzle_text():
	print("""
--- Day 8: Handheld Halting ---
Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.

Their handheld game console won't turn on! They ask if you can take a look.

You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.

The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
For example, consider the following program:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
These instructions are visited in this order:

nop +0  | 1
acc +1  | 2, 8(!)
jmp +4  | 3
acc +3  | 6
jmp -3  | 7
acc -99 |
acc +1  | 4
jmp -4  | 5
acc +6  |
First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2, jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.

This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.

Immediately before the program would run an instruction a second time, the value in the accumulator is 5.

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

--- Part Two ---
After some careful analysis, you believe that exactly one instruction is corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)

The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:

nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6
After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
""")

class testCase(unittest.TestCase):

	def setUp(self):
		self.teststring = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


	def test_basic_action(self):
		self.assertEqual(
			basic_action(self.teststring)[0],
			5
		)
		self.assertEqual(
			basic_action(self.teststring, True)[0],
			8
		)


if __name__ == '__main__':
	try:
		sys.argv[1]
		puzzle_text()

	except:
		input_set = ()
		with open('inputstring_day08.txt') as input_file:
		    input_set = input_file.read()

		print(basic_action(input_set))
		print(basic_action(input_set, True))

	print ("done");

