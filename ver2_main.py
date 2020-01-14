import argparse
import yaml
from modules.latto_crawler import grab_data
from modules.statastic_tools import statastic_plot
MODE = [ \
    "big_latto", \
    "super_latto"
]
def arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-P", "--period", type=int, default=10, \
        help="Stastic Period range (default : 10). For example previous 10 times")
    help_string = "".join(["{}:{}".format(index, MODE[index]) for index in range(len(MODE))])
    parser.add_argument("-M", "--mode", type=int, default=0, help=help_string)
    parser.add_argument("-O", "--output_filepath", type=str, default="result.csv")
    parser.add_argument("-G", "--grab", action="store_true", help="grab information from website")

    args = parser.parse_args()

    print(args)

    return args

def main(args):
    if args.grab:
        grab_data(args)
    statastic_plot(args)

if __name__ == "__main__":
    args = arguments()
    main(args)
