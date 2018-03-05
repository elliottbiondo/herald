from input import read_input
from output import write_output
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("file", type=str,
                    help="the text file database")
    parser.add_argument("person", type=str,
                    help="the person to make the family tree for")
    args = parser.parse_args()
    fam = read_input(args.file)
    write_output(fam, fam[args.person])

if __name__ == '__main__':
    main()
