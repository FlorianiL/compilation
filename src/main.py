import sys
import os

from src.lark_parser import test_lark


def main():
    # Check and retrieve command-line arguments
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    data = sys.argv[1]
    template = sys.argv[2]

    # Verify data file
    if not os.path.isfile(data):
        print("error: {} does not exist".format(data))
        sys.exit(1)

    # Verify template file
    if not os.path.isfile(template):
        print("error: {} does not exist".format(template))
        sys.exit(1)

    test_lark(open(data, "r").read(), open(template, "r").read())


if __name__ == '__main__':
    main()
