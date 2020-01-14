import argparse
import numpy as np
import matplotlib.pyplot as plt
import requests
import time
import pandas as pd
from selenium import webdriver
from lxml import html

output_filename = 'result.csv'
MODE = ["big lattor"]
MODE_MAX_number = {"big lattor":49}
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

def statastic_plot(args):
    csv_path, period, max_bin = args.output_filepath, args.period, MODE_MAX_number[MODE[args.mode]]

    with open(csv_path, "r",encoding='utf-8') as F:
        lines = F.readlines()

    number_l, spec_l = [], []
    for index, line in enumerate(lines):
        if index == 0: continue
        line = line.rstrip()
        l_block = line.split(",")
        id, date, number, special_number = decode_csv_info(l_block)
        number_l.append(number)
        spec_l.append(special_number)

    number_l, spec_l = number_l[:period], spec_l[:period]
    number_l, spec_l = np.array(number_l,dtype=int), np.array(spec_l, dtype=int)

    
    # import pdb;pdb.set_trace()
    plt.figure(0)
    plt.hist(number_l.reshape(-1), bins=max_bin, range=(1,max_bin+1))
    
    plt.title("Normal number distrrbution")

    plt.figure(1)
    plt.hist(spec_l.reshape(-1), bins=max_bin, range=(1,max_bin+1))
    
    plt.title("Special number distrrbution")

    plt.figure(2)
    totally_number = np.concatenate([number_l.reshape(-1), spec_l.reshape(-1)], axis=0)
    plt.hist(totally_number, bins=max_bin, range=(1,max_bin+1))
    plt.title("Totally number distrrbution")

    plt.show()
        
def decode_csv_info(l_block):
    for i in range(len(l_block)):
        if i==1 : continue

    id = l_block[0]
    date = l_block[1]
    number = [ l_block[2], l_block[3], l_block[4], l_block[5], l_block[6], l_block[7]]
    special_number = l_block[8]
    return id, date, number, special_number

def grab_data(args):
    output_filename = args.output_filepath
    url = 'http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'

    req = requests.get(url)
    req.encoding = 'utf-8'

    web_html = html.fromstring(req.content)

    year_list = [y.text for y in web_html.xpath('//*[@id="Lotto649Control_history_dropYear"]/option')]
    month_list = [m.text for m in web_html.xpath('//*[@id="Lotto649Control_history_dropMonth"]/option')]
    year_shift = len(year_list) - 3

    driver = webdriver.Chrome("./chromedriver")

    driver.get(url)

    driver.find_element_by_id('Lotto649Control_history_radYM').click()

    time.sleep(1)

    # output_list = {'日期':[], '第一號碼':[], '第二號碼':[], '第三號碼':[], '第四號碼':[], '第五號碼':[], '第六號碼':[], '特別碼':[],}
    output_list = {'date':[], '1':[], '2':[], '3':[], '4':[], '5':[], '6':[], 'spec':[],}

    for y in range(1 + year_shift,len(year_list)+1):
        
        driver.find_element_by_xpath('//*[@id="Lotto649Control_history_dropYear"]/option['+str(y)+']').click()

        for m in range(1,len(month_list)+1):
            
            driver.find_element_by_xpath('//*[@id="Lotto649Control_history_dropMonth"]/option['+str(m)+']').click()

            driver.find_element_by_id('Lotto649Control_history_btnSubmit').click()

            web_html = html.fromstring(driver.page_source)

            section_i = 0
            while True:
                section = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_SNo1_'+str(section_i)+'"]')
                if len(section) == 0:
                    break

                #this_date = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_L649_DDate_'+str(section_i)+'"]')[0].text
                this_date = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_L649_DDate_'+str(section_i)+'"]')[0].text
                print('%s'%(section_i))
                output_list['date'].append(this_date)
                
                for i in range(1,7):
                    this_number = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_SNo'+str(i)+'_'+str(section_i)+'"]')[0].text
                    print(this_number, end='  ')
                    
                    index = list(output_list.keys())[i]
                    output_list[index].append(this_number)
                    
                last_number = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_No7_'+str(section_i)+'"]')[0].text
                print(last_number)
                output_list['spec'].append(last_number)

                section_i += 1
                print('---')
    driver.quit()
    output = pd.DataFrame([], columns=list(output_list.keys()))
    for k in output_list.keys():
        output[k] = output_list[k]
    output = output.sort_values(ascending=False, by=["date"])
    output.to_csv(output_filename)

    

if __name__ == "__main__":
    args = arguments()
    main(args)
