#!/usr/bin/python
import pdfkit
import json
import subprocess
import argparse
import os.path
import datetime
import string
import random

now = datetime.datetime.now()

CONFIG_PATH = "config.json"
DEFAULT_CONFIG = {
    "name": "[BUSINESS_NAME]",
    "address": "[BUSINESS_ADDRESS]",
    "city_province_country": "[BUSINESS_CITY_PROVINCE_COUNTRY]",
    "postal_code": "[BUSINESS_POSTAL_CODE]",
    "phone": "[BUSINESS_PHONE]",
    "email": "[BUSINESS_EMAIL]",
    "abrv": "[ABRV]",
    "customers": [
        {
            "id": 1,
            "name": "[CUSTOMER_NAME]",
            "address": "[CUSTOMER_ADDRESS]",
            "city_province_country": "[CUSTOMER_CITY_PROVINCE_COUNTRY]",
            "postal_code": "[CUSTOMER_POSTAL_CODE]",
            "phone": "[CUSTOMER_PHONE]"
        }
    ]
}
DEFAULT_DATA = {
    "customer_id": 0,
    "invoice_type": "invoice",
    "invoice_date": "",
    "invoice_number": "",
    "items": [
        {
            "desc": "[DESCRIPTION]",
            "hours": 0,
            "rate": 35,
            "total": 0
        }
    ]
}
INVOICE_NUMBER_UID_LENGTH = 5

parser = argparse.ArgumentParser(description='Generate invoices.')
parser.add_argument('customer_id',
                    help="enter customer id to initialize invoice",
                    nargs='?',
                    const=0)
parser.add_argument("-l", "--list-customers",
                    help="list all customers",
                    action='store_true')
parser.add_argument("-b", "--build",
                    help="build a new pdf using the specified json file",
                    metavar='JSON_FILE',
                    nargs=1)
args = parser.parse_args()


def main():
    config = {}
    if (os.path.isfile(CONFIG_PATH)):
        with open(CONFIG_PATH) as raw_config:
            config = json.load(raw_config)
    else:
        create_json_file(CONFIG_PATH, DEFAULT_CONFIG)
        print("Missing config, please fill it in and try again.")
        open_file(CONFIG_PATH)
        exit()
    if args.list_customers:
        list_customers(config)
    elif args.build:
        data = {}
        if (os.path.isfile(args.build[0])):
            with open(args.build[0]) as raw_data:
                data = json.load(raw_data)
                build_pdf(config, data, args.build[0].replace(".json", ".pdf"))
        else:
            print("Invoice data file '%s' does not exist." % args.build[0])
    elif len([(customer['id'] == args.customer_id) for customer in config['customers']]) > 0:
        init_new_invoice_data(config, get_customer_by_id(config['customers'], args.customer_id))


def list_customers(config):
    for customer in config['customers']:
        print("%s - %s" % (customer['id'], customer['name']))


def build_pdf(config, data, export_path):
    with open("templates/index.html", "r") as file:
        print("Generating...")
        customer = get_customer_by_id(config['customers'], data['customer_id'])
        template = file.read()
        template = template.replace("[BUSINESS_NAME]", config['name']) \
                           .replace("[BUSINESS_ADDRESS]", config['address']) \
                           .replace("[BUSINESS_CITY_PROVINCE_COUNTRY]", config['city_province_country']) \
                           .replace("[BUSINESS_POSTAL_CODE]", config['postal_code']) \
                           .replace("[BUSINESS_PHONE]", config['phone']) \
                           .replace("[CUSTOMER_NAME]", customer['name']) \
                           .replace("[CUSTOMER_ID]", str(customer['id'])) \
                           .replace("[CUSTOMER_ADDRESS]", customer['address']) \
                           .replace("[CUSTOMER_CITY_PROVINCE_COUNTRY]", customer['city_province_country']) \
                           .replace("[CUSTOMER_POSTAL_CODE]", customer['postal_code']) \
                           .replace("[INVOICE_DATE]", data['invoice_date']) \
                           .replace("[INVOICE_NUMBER]", data['invoice_number']) \
                           .replace("[INVOICE_TYPE]", data['invoice_type'], 2) \
                           .replace("[INVOICE_ITEMS]", get_invoice_items(process_invoice_data(data))) \
                           .replace("[INVOICE_SUBTOTAL]", str(get_invoice_subtotal(data))) \
                           .replace("[INVOICE_TOTAL]", str(get_invoice_total(data)))
        pdfkit.from_string(template, export_path)
        subprocess.check_call(["open", "-a", "Preview.app", export_path])
        print("Complete.")


def open_file(path):
    subprocess.check_call(["open", path])


def init_new_invoice_data(config, customer):
    data = DEFAULT_DATA
    data['customer_id'] = customer['id']
    data['invoice_date'] = get_invoice_date(now)
    data['invoice_number'] = get_invoice_number(config['abrv'], now)
    file_name = "%s_-_%s_%s_-_%s.json" % (config['name'].replace(" ", "_"),
                                          customer['name'].replace(" ", "_"),
                                          data['invoice_type'].capitalize(),
                                          data['invoice_number'])
    create_json_file(file_name, data)
    open_file(file_name)


def create_json_file(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)


def get_customer_by_id(customers, customer_id):
    for customer in customers:
        if customer['id'] == int(customer_id):
            return customer
    return None


def get_invoice_number(abbreviation, now):
    return "%s%s%s" % (abbreviation,
                       str(now.strftime("%d%m%Y")),
                       ''.join(random.choices(string.ascii_uppercase + string.digits,
                                              k=INVOICE_NUMBER_UID_LENGTH)))


def get_invoice_date(now):
    return now.strftime("%b %m, %Y")


def get_invoice_items(data):
    out = ""
    for item in data['items']:
        out += "<tr><td>%s</td>" % item['desc']
        out += "<td class='text-right'>%s</td>" % item['hours']
        out += "<td class='text-right'><span class='currency'>$</span>%s</td>" % item['rate']
        out += "<td class='text-right'><span class='currency'>$</span>%s</td></tr>" % item['total']
    return out


def get_invoice_total(data):
    # TODO: Make more comprehensive
    return sum([(item['hours'] * item['rate']) for item in data['items']])

def get_invoice_subtotal(data):
    return sum([(item['hours'] * item['rate']) for item in data['items']])


def process_invoice_data(data):
    for item in data['items']:
        item['total'] = item['hours'] * item['rate']
    return data


if __name__ == '__main__':
    main()