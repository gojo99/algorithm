import numpy as np
import math
from tkinter import *
# creates the window
root = Tk()
# names the window
root.wm_title("Simplex")

ca = np.loadtxt('D:\\function.txt', dtype=int)
inter = np.multiply(ca, -1)
c = inter.tolist()

inter2 = np.loadtxt('D:\\constraints.txt', dtype=int)
a = inter2.tolist()

inter3 = np.loadtxt('D:\\values.txt', dtype=int)
b = inter3.tolist()

def import_files():
    return


def make_tableau(c, a, b):
    xb = [t + [x] for t, x in zip(a, b)]
    z = c + [0]
    return xb + [z]


def can_be_improved(tableau):
    # finds the final row of the tableau
    z = tableau[-1]
    # returns true if any of the values in z are negative, but it excludes the final value.
    can_be = any(x < 0 for x in z[:-1])
    # if true is returned then the optimal solution has not been found, and we continue to perform the pivot operations
    return can_be


def find_pivot_position(tableau):
    # z is assigned the last row of the tableau
    z = tableau[-1]
    # this gives the index of the lowest value in the list
    column = np.argmin(z)

    arr = []
    # runs through all rows except the last row
    for t in tableau[:-1]:
        el = t[column]
        # el_array = np.array(el)
        arr.append(math.inf if el <= 0 else np.array(t[-1]) / np.array(el))
    arr2 = np.array(arr)
    # row = arr.index(min(arr))
    row = np.argmin(arr2)
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


def simplex(c, a, b):
    tableau = make_tableau(c, a, b)

    while can_be_improved(tableau):
        pivot_position = find_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)

    return get_solution(tableau)


solution = simplex(c, a, b)
solution2 = np.round_(solution, decimals = 0)
real_solution = np.array(solution2, dtype='int')
# resu = real_solution*c2*(-1)
# final_resu = np.sum(resu)
# print('solution: ', real_solution)


def click():
    label1 = Label(root, text=real_solution)
    label1.pack()


# button1 = Button(root, text='Import files', command=import_files)
# button2 = Button(root, text='Solve', command=lambda: [make_tableau, can_be_improved, find_pivot_position,
#                                                      pivot_step, is_basic, get_solution, simplex, click])
button3 = Button(root, text='Display results', command=click)


# button1.pack()
# button2.pack()
button3.pack()

root.mainloop()
