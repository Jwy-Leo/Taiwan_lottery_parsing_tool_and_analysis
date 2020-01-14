import os
import numpy as np
import matplotlib.pyplot as plt
MODE = ["big_latto", "super_latto"]
MODE_MAX_number = {
    "big_latto": 49,
    "super_latto": 38
}
def statastic_plot(args):
    # Initial meta information
    _mode_string = MODE[args.mode]
    csv_path, period, max_bin = args.output_filepath, args.period, MODE_MAX_number[_mode_string]
    csv_path = os.path.join("database", "{}_{}".format(_mode_string, csv_path))
    with open(csv_path, "r", encoding='utf-8') as F:
        lines = F.readlines()

    # Aggregate inforamtion together
    number_l, spec_l = [], []
    for index, line in enumerate(lines):
        if index == 0: continue
        line = line.rstrip()
        l_block = line.split(",")
        ID, date, number, special_number = decode_csv_info(args, l_block)
        number_l.append(number)
        spec_l.append(special_number)

    number_l, spec_l = number_l[:period], spec_l[:period]

    number_l, spec_l = np.array(number_l), np.array(spec_l)

    # Plot the result to three figures
    plt.figure(0)
    plt.hist(number_l.reshape(-1), bins=max_bin, range=(1,max_bin+1))
    plt.title("Normal number distribution")
    #plt.xlim(0, max_bin+1)
    plt.figure(1)
    plt.hist(spec_l.reshape(-1), bins=max_bin, range=(1,max_bin+1))
    plt.title("Special number distribution")
    #plt.xlim(0, max_bin+1)
    plt.figure(2)
    totally_number = np.concatenate([number_l.reshape(-1), spec_l.reshape(-1)], axis=0)
    plt.hist(totally_number, bins=max_bin, range=(1,max_bin+1))
    plt.title("Totally number distribution")
    #plt.xlim(0, max_bin+1)
    plt.show()

def decode_csv_info(args, l_block):
    
    for i in range(len(l_block)):
        if i==1: continue

    index = l_block[0]
    date = l_block[1]
    number = [ int(l_block[i]) for i in range(2, len(l_block)-1, 1)]
    special_number = int(l_block[len(l_block)-1])
    return index, date, number, special_number
