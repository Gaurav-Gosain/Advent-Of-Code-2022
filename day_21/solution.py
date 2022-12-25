#!/usr/bin/env python3

from functools import lru_cache
from operator import add, sub, mul, floordiv

OPMAP = {
	'+': add,
	'*': mul,
	'-': sub,
	'/': floordiv
}

REV_OPMAP = {
	('+', True): sub,
	('+', False): sub,
	('*', True): floordiv,
	('*', False): floordiv,
	('-', True): add,
	('-', False): lambda x, l: l - x,
	('/', True): mul,
	('/', False): lambda x, l: l // x,
}


def is_tree():
	seen = set(T)

	for v in T.values():
		if isinstance(v, int):
			continue

		try:
			seen.remove(v[0])
			seen.remove(v[2])
		except KeyError:
			return False

	return True


@lru_cache()
def calc(node):
	value = T[node]
	if not isinstance(value, list):
		return value

	l, op, r = value
	lvalue = calc(l)
	rvalue = calc(r)

	if lvalue is None or rvalue is None:
		return None
	return OPMAP[op](lvalue, rvalue)


def find_value(node, expected):
	if node == 'humn':
		return expected

	l, op, r = T[node]
	lvalue = calc(l)
	rvalue = calc(r)

	if lvalue is None:
		return find_value(l, REV_OPMAP[op, True](expected, rvalue))
	return find_value(r, REV_OPMAP[op, False](expected, lvalue))


T = {}
for line in open("input/input.txt").read().splitlines():
	a, b = line.strip().split(': ')
	T[a] = int(b) if b.isdigit() else b.split()

answer = calc('root')
print(1, answer)


assert is_tree(T), 'This solution assumes the input is a well-formed tree!'

T['humn'] = None
T['root'][1] = '-'
calc.cache_clear()

answer = find_value('root', 0)
print(2, answer)
