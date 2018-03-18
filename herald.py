from os import system

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
    output_file = "fam"
    write_output(fam, fam[args.person], output_file)
    system("inkscape {0}.svg --export-pdf {0}.pdf".format(output_file))



if __name__ == '__main__':
    main()
