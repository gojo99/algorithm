import numpy as np
import math

function = [int(n) for n in input('Enter coefficients of the function and add 0s for '
                                  'each slack \ surplus ''variables: ').split()]
function2 = np.array(function)
np.savetxt('function.txt', function2, fmt='%d')
ca = np.loadtxt('function.txt', dtype=int)
inter = np.multiply(ca, -1)
c = inter.tolist()
c2 = c + [0]

r = int(input('How many constraints do you have: '))
# initializing an empty matrix
arr = []
# taking 2x2 matrix from the user
for i in range(r):
    # taking row input from the user
    row = list(map(int, input('Enter the constraints and add +1 for slack and -1 for surplus variables'
                              ' at the correct positions: ').split()))
    # appending the 'row' to the 'matrix'
    arr.append(row)

arr2 = np.array(arr)
np.savetxt('constraints.txt', arr2, fmt='%d')
inter2 = np.loadtxt('constraints.txt', dtype=int)
a = inter2.tolist()

brrr = [int(n) for n in input('Enter the value for each constraint inequality: ').split()]
arr3 = np.array(brrr)
np.savetxt('constraints_values.txt', arr3, fmt='%d')
inter3 = np.loadtxt('constraints_values.txt', dtype=int)
b = inter3.tolist()


# create the tableau
def make_tableau(c2, a, b):
    xb = [t + [x] for t, x in zip(a, b)]
    z = c + [0]
    return xb + [z]


def can_be_improved(tableau):
    z = tableau[-1]
    can_be = any(x < 0 for x in z[:-1])
    return can_be


def find_pivot_position(tableau):
    z = tableau[-1]
    column = np.argmin(z)

    arr = []
    for t in tableau[:-1]:
        el = t[column]
        arr.append(math.inf if el <= 0 else t[-1] / el)

    row = arr.index(min(arr))
    return row, column


def pivot_step(tableau, pivot_position):
    new_tableau = [[] for t in tableau]

    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value

    for t_i, t in enumerate(tableau):
        if t_i != i:
            row_op = np.array(new_tableau[i]) * tableau[t_i][j]
            new_tableau[t_i] = np.array(tableau[t_i]) - row_op

    return new_tableau


def is_basic(column):
    m = sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1
    return m


def get_solution(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)

    return solutions


def simplex(c2, a, b):
    tableau = make_tableau(c2, a, b)

    while can_be_improved(tableau):
        pivot_position = find_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)

    return get_solution(tableau)


simplex(c2, a, b)
solution = simplex(c2, a, b)
real_solution = np.array(solution, dtype='int')
resu = real_solution*c2*(-1)
final_resu = np.sum(resu)


print('solution: ', real_solution)
print('Profit: ', final_resu)