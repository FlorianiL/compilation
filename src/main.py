import sys
import os


def main():
    # Check and retrieve command-line arguments
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)  # Return a non-zero value to indicate abnormal termination
    fileData = sys.argv[1]
    fileTemplate = sys.argv[2]

    # Verify data file
    if not os.path.isfile(fileData):
        print("error: {} does not exist".format(fileData))
        sys.exit(1)

    # Verify template file
    if not os.path.isfile(fileTemplate):
        print("error: {} does not exist".format(fileTemplate))
        sys.exit(1)

    # Process the file line-by-line
    with open(fileData, 'r') as data, open(fileTemplate, 'r') as template:
        line_number = 0
        for line in data:
            line_number += 1
            line = line.rstrip()
            print(line)
        print("Number of lines: {}\n".format(line_number))


if __name__ == '__main__':
    main()
