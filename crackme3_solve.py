#!/usr/bin/env python2

# Author: Ben Denton (ben@bendenton.com) | 16 May 2018
# Solves "crackme3" from https://github.com/holbertonschool/dont_hate_the_hacker_hate_the_code

# run ./crackme "$(<crackme_solution)" after executing this script to  verify
# Hurray!

import angr
import claripy

def main():
    target = "./crackme3"
    proj = angr.Project(target)

    argv1 = claripy.BVS("argv1", 4 * 8) # declare argv[1], as a symbolic bit vector.  This is the password input from the user.
                                        # the strlen checks if the password == 4, set the BV to 4 bytes

    initial_state = proj.factory.entry_state(args=[target, argv1])

    sm = proj.factory.simulation_manager(initial_state)

    find_addr = 0x400685
    avoid_addr = [0x4006f5, 0x40062b]

    sm.explore(find=find_addr, avoid=avoid_addr)
    found = sm.found[0]

    solution = found.solver.eval(argv1, cast_to=str)

    f=open("crackme3_solution","wb")
    f.write(solution)
    f.close()

    return solution

if __name__ == '__main__':
    print(repr(main()))