# This script contains functions specific to the paper Grafos de Partición. In particular,
# functions for adding and multiplying in the paper's algebraic structure are given.
# Here, we will consider an element of the partition space to be an array of the form
# [ [m_1,[a_1]] , [m_2,[a_2]] , ... [m_n,[a_n]] ] where m_i is the scalar factor
# of the i-th partition, and a_i is an actual partition of n.

import os

def lam (n):
	if n % 2 == 0:
		return int((n/2))
	else:
		return int(((n-1)/2))

def part_count(A):
	C = max(A) * [0]
	for i in range(len(A)):
		C[A[i]-1] = C[A[i]-1] + 1
	return C

def part_compare(A,B):
	if part_count(A) == part_count(B):
		return True
	else:
		return False

def elem_sum(A,B):
	return A+B

def elem_product(A_elem,B_elem):
	C_scalar = A_elem[0]*B_elem[0]
	C_elem = [C_scalar,A_elem[1]+B_elem[1]]
	return C_elem

def elem_simplify(A,B):
	if part_compare(A[1],B[1]):
		return [A[0] + B[0],A[1]]
	else:
		return False

def rep_simplify(A):
	for i in range(len(A)-1):
		for j in range(len(A)):
			if j > i:
				try:
					if part_compare(A[i][1],A[j][1]):
						A[i] = elem_simplify(A[i],A[j])
						A.pop(j)
					else:
						continue
				except IndexError:
					continue
			else:
				continue
	return A

def rep_product(A,B):
	C = []
	for i in range(len(A)):
		for j in range(len(B)):
			C.append(elem_product(A[i],B[j]))

	return rep_simplify(C)

def r(n):
	if n == 1:
		return [[1,[1]]]
	if n == 2:
		return [[1,[2]],[1,[1,1]]]
	if n == 3:
		return [[1,[3]],[1,[1,2]],[1,[1,1,1]]]
	else:
		N = [[1,[n]]]
		for j in range(lam(n)):
			N = N + rep_product(r(j+1),r(n-(j+1)))
		return rep_simplify(N)

def pprint(A):
	for j in range(len(A)):
		print(A[j])

def clear():
	if os.name == "nt":
		_=os.system("cls")
	else:
		_=os.system("clear")

def part_scalar_sum(A):
	avg_sum = 0
	for i in range(len(A)):
		avg_sum = avg_sum + A[i][0]
	return avg_sum

def eta(n):
	if n == 1:
		return 1
	if n == 2:
		return 1
	if n == 3:
		return 1
	else:
		N = 0
		for j in range(lam(n)):
			N = N + eta(j+1) * eta(n-(j+1))
		return N

def terms(n):
	preloaded_values = [1,2,3,8,15,41,96,288,724,2142,5838,17720,49871,151846,440915]
	if n <= 15:
		return preloaded_values[n-1]
	term_sum = 0
	for j in range(lam(n)):
		term_sum = term_sum + terms(j+1)*terms(n-(j+1))
	return term_sum + 1


def spnum(A):
	if A <= 0:
		return 0
	else:
		return int((2*A -1 + pow(-1,A))/4)



