import os
import requests
from selenium import webdriver
import pandas as pd
from lxml import html
import time

def grab_data(args):
    # Initial meta information
    
    mode_index = args["control"]['mode']
    output_filename = args['control']['output_filepath']
    _mode_string = args["Lottery_categories"][mode_index]
    url = args[_mode_string]["Parsing_URL_SET"]
    component_prefix = args[_mode_string]["Parsing_switch_page_component"]
    date_component_id = args[_mode_string]["Parsing_date_component"]

    # Interactive with page
    # Fetch meta information
    req = requests.get(url)
    req.encoding = 'utf-8'
    web_html = html.fromstring(req.content)
    _x_path = '//*[@id="{}_{}"]/option'.format(component_prefix, "dropYear")
    year_list = [y.text for y in web_html.xpath(_x_path)]
    _x_path = '//*[@id="{}_{}"]/option'.format(component_prefix, "dropMonth")
    month_list = [m.text for m in web_html.xpath(_x_path)]
    year_shift = len(year_list) - 3
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome("./chromedriver")
    driver.get(url)
    driver.find_element_by_id("{}_{}".format(component_prefix, "radYM")).click()
    time.sleep(1)
    output_list = {"date":[], "spec":[]}
    # Fetch unit information
    for y in range(1 + year_shift, len(year_list)+1):
        _x_path = '//*[@id="{}_{}"]/option[{}]'.format(component_prefix, "dropYear", str(y))
        driver.find_element_by_xpath(_x_path).click()
        for m in range(1, len(month_list)+1):
            _x_path = '//*[@id="{}_{}"]/option[{}]'.format(component_prefix, "dropMonth", str(m))
            driver.find_element_by_xpath(_x_path).click()
            btn_id = '{}_{}'.format(component_prefix, "btnSubmit")
            driver.find_element_by_id(btn_id).click()
            web_html = html.fromstring(driver.page_source)

            section_i = 0
            while True:
                _x_path = '//*[@id="{}_{}_{}"]'.format(component_prefix, "dlQuery_SNo1",str(section_i))
                section = web_html.xpath(_x_path)
                if len(section) == 0: break

                _x_path = '//*[@id="{}_{}_{}"]'.format(component_prefix, date_component_id,str(section_i))
                this_date = web_html.xpath(_x_path)[0].text
                print("{}".format(section_i))
                output_list['date'].append(this_date)
                
                for i in range(1,7):

                    _x_path = '//*[@id="{}_{}_{}"]'.format(component_prefix, "dlQuery_SNo{}".format(i), section_i)
                    this_number = web_html.xpath(_x_path)[0].text
                    print(this_number)
                    
                    #index = list(output_list.keys())[i]
                    if str(i) not in output_list.keys():
                        output_list[str(i)] = []
                    output_list[str(i)].append(this_number)

                _x_path = '//*[@id="{}_{}_{}"]'.format(component_prefix, "dlQuery_No7", section_i)
                last_number = web_html.xpath(_x_path)[0].text
                print(last_number)
                output_list['spec'].append(last_number)
                
                section_i += 1
                print("---")
    driver.quit()
    # Save the data
    output=pd.DataFrame([], columns=list(output_list.keys()))
    for k in output_list.keys():
        output[k] = output_list[k]
    output = output.sort_values(ascending=False, by=["date"])
    #output.to_csv(output_filename)
    output_filename = _mode_string + "_" + output_filename
    output_filename = os.path.join("database", output_filename)
    if not os.path.exists("database"):
        os.makedirs("database") 
    output.to_csv(output_filename)
