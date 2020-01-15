import argparse
import yaml
from modules.lottery_crawler import grab_data
from modules.statastic_tools import statastic_plot
def arguments():
    with open("config/Option_command.yaml", "r") as F:
        y_args = yaml.load(F)

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-P", "--period", type=int, default=10, \
        help="Stastic Period range (default : 10). For example previous 10 times")
    help_string = "\n".join(["{}:{}".format(index, y_args["Lottery_categories"][index]) for index in range(len(y_args['Lottery_categories']))])
    parser.add_argument("-M", "--mode", type=int, default=0, help=help_string)
    parser.add_argument("-O", "--output_filepath", type=str, default="result.csv")
    parser.add_argument("-G", "--grab", action="store_true", help="grab information from website")

    args = parser.parse_args()

    print(args)

    control_vars = vars(args)
    y_args["control"] = {}
    for c_key in control_vars.keys():
        y_args["control"][c_key] = control_vars[c_key]

    return y_args

def main(args):
    if args['control']['grab']:
        grab_data(args)
    statastic_plot(args)

if __name__ == "__main__":
    args = arguments()
    main(args)
