import csv
import requests
from bs4 import BeautifulSoup
import shutil
from tempfile import NamedTemporaryFile
import time
import re
import random
import pandas as pd
import urllib.request as req

CSV_FILE = 'PIN_Multi.csv'

# Parameters for POST request
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'content-type': 'text/xml'
}

URL = 'http://kaneil.devnetwedge.com/Search/ExecuteSearch'
# URL = 'http://mchenryil.devnetwedge.com/Search/ExecuteSearch'
# URL = 'http://kendallil.devnetwedge.com/Search/ExecuteSearch'

"""Dataframe to handle easy CSV or Excel filemakings"""
dataframe = pd.DataFrame(columns=['PIN',
                                  'site_address_1',
                                  'site_address_2',
                                  'site_address_3',
                                  'site_address_4',
                                  'owner_and_address_1',
                                  'owner_and_address_2',
                                  'owner_and_address_3',
                                  'owner_and_address_4',
                                  'owner_and_address_5',
                                  'tax_year',
                                  'sale_status',
                                  'property_class',
                                  'mailing_address',
                                  'sales_year',
                                  'sales_doc',
                                  'sales_type',
                                  'sales_date',
                                  'sales_by',
                                  'sales_to',
                                  'sales_gross',
                                  'sales_prop',
                                  'sales_net',
                                  'exem_type',
                                  'exem_date',
                                  'gran_date',
                                  'renew_date',
                                  'pro_date ',
                                  'req_amnt ',
                                  'gran_amnt',
                                  'red_year',
                                  'red_cert',
                                  'red_type',
                                  'red_sold',
                                  'red_sale',
                                  'red_date',
                                  'red_pena'])

CSV_HEADER = [
    'PIN',
    'site_address_1',
    'site_address_2',
    'site_address_3',
    'site_address_4',
    'owner_and_address_1',
    'owner_and_address_2',
    'owner_and_address_3',
    'owner_and_address_4',
    'owner_and_address_5',
    'tax_year',
    'sale_status',
    'property_class',
    'mailing_address',
    'sales_year',
    'sales_doc',
    'sales_type',
    'sales_date',
    'sales_by',
    'sales_to',
    'sales_gross',
    'sales_prop',
    'sales_net',
    'exem_type',
    'exem_date',
    'gran_date',
    'renew_date',
    'pro_date ',
    'req_amnt ',
    'gran_amnt',
    'red_year',
    'red_cert',
    'red_type',
    'red_sold',
    'red_sale',
    'red_date',
    'red_pena'
]


def get_pins(csv_file):
    with open(csv_file) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        pins = [pin[0] for pin in csvreader]
        return pins  # -> list


def dump_to_csv(csv_file, d_data):
    fieldnames = CSV_HEADER
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    with open(csv_file, 'r', newline='') as csvfile, tempfile:
        reader = csv.DictReader(
            csvfile, fieldnames=fieldnames, lineterminator='\n', delimiter=',')
        writer = csv.DictWriter(
            tempfile, fieldnames=fieldnames, lineterminator='\n', delimiter=',')
        for row in reader:
            if row['PIN'] == d_data['PIN']:
                row = d_data
            writer.writerow(row)
    shutil.move(tempfile.name, csv_file)


def l_to_csv(l):
    # list concat func
    try:
        return (';'.join(l))
    except:
        print('Exception at line 125')


def loop_td_rows(table, td_index, fix=False, forced_tr_class=None):
    #Func to extract data from table, fix toggle for unclosed html tag
    data = []
    # print(td_index)
    try:
        if forced_tr_class:
            tr = table.tbody.find_all('tr', {'class': forced_tr_class})
        else:
            tr = table.tbody.find_all('tr')
        for row in tr:
            if fix:
                data.append(
                    (row.find_all('td')[td_index].text.strip().split('\n')[0]))
                # print(row.find_all('td')[td_index].text.strip().split('\n')[0])
            else:
                data.append((row.find_all('td')[td_index].text.strip()))
                # print(row.find_all('td')[td_index].text.strip())
    except:
        return '-'
    # print(data)
    return data

# 2 - get page (token) then post data for specified pin


def get_taxes(pin, Search_URL):
    # Get session TOKEN
    s = requests.Session()

    try:
        no_dash_pin = pin.replace("-", '')
    except:
        no_dash_pin = pin
    # print(no_dash_pin)

    data = {
        'property_key': no_dash_pin
    }

    # find if returns multiple instances or empty
    b = req.urlopen(url=Search_URL+"{0}".format(no_dash_pin))
    soup = BeautifulSoup(b, 'html.parser')
    search_res = soup.find('h3', string='Search Results')
    print(Search_URL+"{0}".format(no_dash_pin))
    if True:
        c = req.urlopen(Search_URL+"{0}".format(no_dash_pin))
        return c  # -> html response

    return b  # -> html response


def parse_html(requests_resp, pin):
    html = requests_resp
    soup = BeautifulSoup(html, 'html.parser')

    property_res = soup.find('h3', string='Property Information')
    if property_res:
        pass
    else:
        dict_data = {
            'PIN': pin,
            'site_address_1': 'SERVER ERROR - PIN NOT FOUND',
            'site_address_2': '-',
            'site_address_3': '-',
            'site_address_4': '-',
            'owner_and_address_1': '-',
            'owner_and_address_2': '-',
            'owner_and_address_3': '-',
            'owner_and_address_4': '-',
            'owner_and_address_5': '-',
            'tax_year': '-',
            'sale_status': '-',
            'property_class': '-',
            'mailing_address': '-',
            'sales_year': '-',
            'sales_doc': '-',
            'sales_type': '-',
            'sales_date': '-',
            'sales_by': '-',
            'sales_to': '-',
            'sales_gross': '-',
            'sales_prop': '-',
            'sales_net': '-',
            'exem_type': '-',
            'exem_date': '-',
            'gran_date': '-',
            'renew_date': '-',
            'pro_date ': '-',
            'req_amnt ': '-',
            'gran_amnt': '-',
            'red_year': '-',
            'red_cert': '-',
            'red_type': '-',
            'red_sold': '-',
            'red_sale': '-',
            'red_date': '-',
            'red_pena': '-'
        }
        return dict_data

    try:
        table1 = soup.find_all('table', {'class': 'table table-bordered'})[0]
        site_address = table1.tr.find_all('td')[1].find(
            'div', {'class': 'inner-value'}).text.strip().split('\n')

        try:
            # print("2 should be here: ", len(site_address))
            if (len(site_address) >= 2):
                site_address_1 = re.sub("\s+", " ", site_address[0].strip())
                site_address_2_34 = re.sub(
                    "\s+", " ", site_address[1].strip()).split(',')
                site_address_2 = site_address_2_34[0].strip(', ')
                if (site_address_2) == '':
                    site_address_2 = '-'
                if (len(site_address_2_34) > 1):
                    site_address_34 = re.sub(
                        "\s+", " ", site_address_2_34[1].strip()).split(' ')
                else:
                    site_address_34 = '-'

                if (len(site_address_34) >= 2):
                    site_address_3 = site_address_34[0].strip(', ')
                    site_address_4 = site_address_34[1].strip(', ')
                    site_address_4 = int(site_address_4)
                else:
                    site_address_3 = '-'
                    site_address_4 = '-'
            else:
                site_address_1 = '-'
                site_address_4 = '-'
                site_address_34 = '-'
                site_address_2 = '-'
                site_address_3 = '-'
                site_address_2_34 = '-'
        except:
            print('Error was at 258')

        # print(site_address_1)
        # print(site_address_2)
        # print(site_address_3)
        # print(site_address_4)

        owner_and_address = table1.tr.find_all('td')[2].find(
            'div', {'class': 'inner-value'}).text.strip().split('\n')
        owner_and_address_1 = re.sub("\s+", " ", owner_and_address[0].strip())

        if (len(owner_and_address) >= 2):
            owner_and_address_2 = re.sub(
                "\s+", " ", owner_and_address[-2].strip())
            owner_and_address_345 = re.sub(
                "\s+", " ", owner_and_address[-1].strip()).split(',')
            if owner_and_address[1] != owner_and_address_2:
                # print("New address is found")
                owner_and_address_1 = owner_and_address_1 + \
                    " " + owner_and_address[1]
        else:
            owner_and_address_1 = '-'
            owner_and_address_2 = '-'
            owner_and_address_345 = '-'


        # print(owner_and_address_1)
        if (len(owner_and_address_345) == 3):
            owner_and_address_3 = owner_and_address_345[0].strip(', ')
            owner_and_address_4 = owner_and_address_345[1].strip(', ')
            owner_and_address_5 = owner_and_address_345[2].strip(', ')
        else:
            owner_and_address_3 = '-'
            owner_and_address_4 = '-'
            owner_and_address_5 = '-'

        # owner_and_address = re.sub("\s+", " ", owner_and_address)

        tax_year = table1.find_all('tr')[1].find_all('td')[0].find(
            'div', {'class': 'inner-value'}).find('div').text.strip()

        sale_status = table1.find_all('tr')[2].find_all('td')[0].find(
            'div', {'class': 'inner-value'}).find('p').text.strip()

        property_class = table1.find_all('tr')[3].find_all(
            'td')[0].find('div', {'class': 'inner-value'}).text.strip()

        mailing_address = table1.find_all('tr')[5].find_all(
            'td')[2].find('div', {'class': 'inner-value'}).text.strip()

        """Sales history"""
        try:
            sales_table = soup.find('h3', string='Sales History').parent.parent.find_all(
                'table', {'class': 'table table-bordered table-hover'})[0]
            try:
                sales_year = l_to_csv(loop_td_rows(sales_table, 0))
                # sales_year = (loop_td_rows(sales_table, 0))[0]
            except:
                sales_year = '-'
            try:
                sales_doc = l_to_csv(loop_td_rows(sales_table, 1))
            except:
                sales_doc = '-'
            try:
                sales_type = l_to_csv(loop_td_rows(sales_table, 2))
            except:
                sales_type = '-'
            try:
                sales_date = l_to_csv(loop_td_rows(sales_table, 3))
            except:
                sales_date = '-'
            try:
                sales_by = l_to_csv(loop_td_rows(sales_table, 4))
                if sales_by == '':
                    sales_by = '-'
            except:
                sales_by = '-'
            try:
                sales_to = l_to_csv(loop_td_rows(sales_table, 5))
                if sales_to == '':
                    sales_to = '-'
            except:
                sales_to = '-'
            try:
                sales_gross = l_to_csv(loop_td_rows(sales_table, 6))
            except:
                sales_gross = '-'
            try:
                sales_prop = l_to_csv(loop_td_rows(sales_table, 7))
            except:
                sales_prop = '-'
            try:
                sales_net = l_to_csv(loop_td_rows(sales_table, 8))
            except:
                sales_net = '-'

        except Exception as error:
            sales_year = '-'
            sales_doc = '-'
            sales_type = '-'
            sales_date = '-'
            sales_by = '-'
            sales_to = '-'
            sales_gross = '-'
            sales_prop = '-'
            sales_net = '-'

        """Exemptions"""
        try:
            extemptions_table = soup.find('h3', text=re.compile(r'Exemptions')).parent.parent.find_all(
                'table', {'class': 'table table-bordered table-hover'})[0]
            try:
                exem_type = l_to_csv(loop_td_rows(extemptions_table, 0))
            except:
                exem_type = '-'
            try:
                exem_date = l_to_csv(loop_td_rows(extemptions_table, 1))
            except:
                exem_date = '-'
            try:
                gran_date = l_to_csv(loop_td_rows(extemptions_table, 2))
            except:
                gran_date = '-'
            try:
                renew_date = l_to_csv(loop_td_rows(extemptions_table, 3))
            except:
                renew_date = '-'
            try:
                pro_date = l_to_csv(loop_td_rows(extemptions_table, 4))
            except:
                pro_date = '-'
            try:
                req_amnt = l_to_csv(loop_td_rows(extemptions_table, 5))
            except:
                req_amnt = '-'
            try:
                gran_amnt = l_to_csv(loop_td_rows(extemptions_table, 6))
            except:
                gran_amnt = '-'

        except AttributeError:
            # print('Changed the letters at Exemption')
            extemptions_table = soup.find('h3', text=re.compile(r'Exemption')).parent.parent.find_all(
                'table', {'class': 'table table-bordered table-hover'})[0]
            try:
                exem_type = l_to_csv(loop_td_rows(extemptions_table, 0))
            except:
                exem_type = '-'
            try:
                exem_date = l_to_csv(loop_td_rows(extemptions_table, 1))
            except:
                exem_date = '-'
            try:
                gran_date = l_to_csv(loop_td_rows(extemptions_table, 2))
            except:
                gran_date = '-'
            try:
                renew_date = l_to_csv(loop_td_rows(extemptions_table, 3))
            except:
                renew_date = '-'
            try:
                pro_date = l_to_csv(loop_td_rows(extemptions_table, 4))
            except:
                pro_date = '-'
            try:
                req_amnt = l_to_csv(loop_td_rows(extemptions_table, 5))
            except:
                req_amnt = '-'
            try:
                gran_amnt = l_to_csv(loop_td_rows(extemptions_table, 6))
            except:
                gran_amnt = '-'

        except IndexError:
            exem_type = '-'
            exem_date = '-'
            gran_date = '-'
            renew_date = '-'
            pro_date = '-'
            req_amnt = '-'
            gran_amnt = '-'

        """Redemption"""
        try:
            redemptions_table = soup.find('h3', text=re.compile(r'Redemptions')).parent.parent.find_all(
                'table', {'class': 'table table-bordered table-hover'})[0]
            try:
                red_year = l_to_csv(loop_td_rows(
                    redemptions_table, 0, forced_tr_class='text-center'))
            except:
                red_year = '-'
            try:
                red_cert = l_to_csv(loop_td_rows(
                    redemptions_table, 1, forced_tr_class='text-center'))
            except:
                red_cert = '-'
            try:
                red_type = l_to_csv(loop_td_rows(
                    redemptions_table, 2, forced_tr_class='text-center'))
            except:
                red_type = '-'
            try:
                red_sold = l_to_csv(loop_td_rows(
                    redemptions_table, 3, forced_tr_class='text-center'))
            except:
                red_sold = '-'
            try:
                red_sale = l_to_csv(loop_td_rows(
                    redemptions_table, 4, forced_tr_class='text-center'))
            except:
                red_sale = '-'
            try:
                red_date = l_to_csv(loop_td_rows(
                    redemptions_table, 5, forced_tr_class='text-center'))
                if red_date == '':
                    red_date = '-'
            except:
                red_date = '-'
            try:
                red_pena = l_to_csv(loop_td_rows(
                    redemptions_table, 6, forced_tr_class='text-center'))
            except:
                red_pena = '-'

        except AttributeError:
            # print("Changed letters at Redemption")
            redemptions_table = soup.find('h3', text=re.compile(r'Redemption')).parent.parent.find_all(
                'table', {'class': 'table table-bordered table-hover'})[0]
            try:
                red_year = l_to_csv(loop_td_rows(
                    redemptions_table, 0, forced_tr_class='text-center'))
            except:
                red_year = '-'
            try:
                red_cert = l_to_csv(loop_td_rows(
                    redemptions_table, 1, forced_tr_class='text-center'))
            except:
                red_cert = '-'
            try:
                red_type = l_to_csv(loop_td_rows(
                    redemptions_table, 2, forced_tr_class='text-center'))
            except:
                red_type = '-'
            try:
                red_sold = l_to_csv(loop_td_rows(
                    redemptions_table, 3, forced_tr_class='text-center'))
            except:
                red_sold = '-'
            try:
                red_sale = l_to_csv(loop_td_rows(
                    redemptions_table, 4, forced_tr_class='text-center'))
            except:
                red_sale = '-'
            try:
                red_date = l_to_csv(loop_td_rows(
                    redemptions_table, 5, forced_tr_class='text-center'))
                if red_date == '':
                    red_date = '-'
            except:
                red_date = '-'
            try:
                red_pena = l_to_csv(loop_td_rows(
                    redemptions_table, 6, forced_tr_class='text-center'))
            except:
                red_pena = '-'

        except IndexError:
            red_year = '-'
            red_cert = '-'
            red_type = '-'
            red_sold = '-'
            red_sale = '-'
            red_date = '-'
            red_pena = '-'

        dict_data = {
            'PIN': pin,
            'site_address_1': site_address_1,
            'site_address_2': site_address_2,
            'site_address_3': site_address_3,
            'site_address_4': site_address_4,
            'owner_and_address_1': owner_and_address_1,
            'owner_and_address_2': owner_and_address_2,
            'owner_and_address_3': owner_and_address_3,
            'owner_and_address_4': owner_and_address_4,
            'owner_and_address_5': owner_and_address_5,
            'tax_year': tax_year,
            'sale_status': sale_status,
            'property_class': property_class,
            'mailing_address': mailing_address,
            'sales_year': sales_year,
            'sales_doc': sales_doc,
            'sales_type': sales_type,
            'sales_date': sales_date,
            'sales_by': sales_by,
            'sales_to': sales_to,
            'sales_gross': sales_gross,
            'sales_prop': sales_prop,
            'sales_net': sales_net,
            'exem_type': exem_type,
            'exem_date': exem_date,
            'gran_date': gran_date,
            'renew_date': renew_date,
            'pro_date ': pro_date,
            'req_amnt ': req_amnt,
            'gran_amnt': gran_amnt,
            'red_year': red_year,
            'red_cert': red_cert,
            'red_type': red_type,
            'red_sold': red_sold,
            'red_sale': red_sale,
            'red_date': red_date,
            'red_pena': red_pena
        }

    except TimeoutError:
        dict_data = {
            'PIN': pin,
            'site_address_1': "Row was skipped due to timeout error",
            'site_address_2': '-',
            'site_address_3': '-',
            'site_address_4': '-',
            'owner_and_address_1': '-',
            'owner_and_address_2': '-',
            'owner_and_address_3': '-',
            'owner_and_address_4': '-',
            'owner_and_address_5': '-',
            'tax_year': '-',
            'sale_status': '-',
            'property_class': '-',
            'mailing_address': '-',
            'sales_year': '-',
            'sales_doc': '-',
            'sales_type': '-',
            'sales_date': '-',
            'sales_by': '-',
            'sales_to': '-',
            'sales_gross': '-',
            'sales_prop': '-',
            'sales_net': '-',
            'exem_type': '-',
            'exem_date': '-',
            'gran_date': '-',
            'renew_date': '-',
            'pro_date ': '-',
            'req_amnt ': '-',
            'gran_amnt': '-',
            'red_year': '-',
            'red_cert': '-',
            'red_type': '-',
            'red_sold': '-',
            'red_sale': '-',
            'red_date': '-',
            'red_pena': '-'
        }

    except Exception as error:
        dict_data = {
            'PIN': pin,
            'site_address_1': error,
            'site_address_2': '-',
            'site_address_3': '-',
            'site_address_4': '-',
            'owner_and_address_1': '-',
            'owner_and_address_2': '-',
            'owner_and_address_3': '-',
            'owner_and_address_4': '-',
            'owner_and_address_5': '-',
            'tax_year': '-',
            'sale_status': '-',
            'property_class': '-',
            'mailing_address': '-',
            'sales_year': '-',
            'sales_doc': '-',
            'sales_type': '-',
            'sales_date': '-',
            'sales_by': '-',
            'sales_to': '-',
            'sales_gross': '-',
            'sales_prop': '-',
            'sales_net': '-',
            'exem_type': '-',
            'exem_date': '-',
            'gran_date': '-',
            'renew_date': '-',
            'pro_date ': '-',
            'req_amnt ': '-',
            'gran_amnt': '-',
            'red_year': '-',
            'red_cert': '-',
            'red_type': '-',
            'red_sold': '-',
            'red_sale': '-',
            'red_date': '-',
            'red_pena': '-'
        }

    return dict_data


def get_county_data():
    County_name = input(
        """Select an option (1,2,3,....):\n1. Kane\n2. Kendall\n3. Mchenry\n\n""")

    print("""###################\n\n""")

    if County_name == "1":  # -> Kane
        Search_URL = 'http://kaneil.devnetwedge.com/parcel/view/'
        URL = 'http://kaneil.devnetwedge.com/Search/ExecuteSearch'
        return Search_URL

    elif County_name == "2":  # -> Kendall
        Search_URL = 'http://kendallil.devnetwedge.com/parcel/view/'
        URL = 'http://kendallil.devnetwedge.com/Search/ExecuteSearch'
        return Search_URL

    elif County_name == "3":  # -> Mchenry
        Search_URL = 'http://mchenryil.devnetwedge.com/parcel/view/'
        URL = 'http://mchenryil.devnetwedge.com/Search/ExecuteSearch'
        return Search_URL
    else:
        return 'No url', 'No Search URL'


if __name__ == "__main__":
    """CORE SCRIPT"""

    Search_URL = get_county_data()
    pins = get_pins(CSV_FILE)

    for pin in pins:
        print("{0}, {1}".format(pin, pins.index(pin) + 1))
        response = get_taxes(pin, Search_URL)
        dict_data = parse_html(response, pin)
        """Commented below line to not change the csv file being read"""
        # dump_to_csv(CSV_FILE, dict_data)
        dataframe = dataframe.append(dict_data, ignore_index=True)

"""Name the Excel file you want to create as a result of the script"""
dataframe.to_excel('Kane.xlsx', index=False)

# """ONLY FOR TEST - TESTING SCRIPT"""
# # pin = '02-33-251-001'
# # for i in range(1):
# #     print("OPS n.: {0}".format(i+1))
# #     response = get_taxes(pin)
# #     dict_data = parse_html(response, pin)
# #     print(dict_data['site_address_1'])
# #     print(dict_data['site_address_2'])
# #     print(dict_data['site_address_3'])
# #     print(dict_data['site_address_4'])

# #     print("##############")

# #     print(dict_data['owner_and_address_1'])
# #     print(dict_data['owner_and_address_2'])
# #     print(dict_data['owner_and_address_3'])
# #     print(dict_data['owner_and_address_4'])
# #     print(dict_data['owner_and_address_5'])

# """ONLY FOR TEST - TESTING PARAMS"""
# # CSV_FILE = 'PIN_TEST.csv'  # uncomment for testing!!
