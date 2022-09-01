# pylint: disable=missing-module-docstring,missing-function-docstring,eval-used
import sys

import operator

def main():
    """Implement the calculator"""


    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,  # use operator.div for Python 2
        '%': operator.mod,
        '^': operator.xor,
    }
    # print(ops[sys.argv[2]])
    # result = sys.argv[1] + ops[sys.argv[2]] + sys.argv[3]
    result = ops[sys.argv[2]](int(sys.argv[1]), int(sys.argv[3]))
    return result

if __name__ == "__main__":
    print(main())
    
