#!/usr/bin/python
import pdfkit
import yaml
import subprocess
import argparse
import os.path
import datetime
import string
import random
import sys

now = datetime.datetime.now()

CONFIG_PATH = "config.yaml"
INVOICE_NUMBER_UID_LENGTH = 5
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
        }
    ]
}
DEFAULT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>Invoice Gen</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <link href="https://fonts.googleapis.com/css?family=Titillium+Web:200,300,400,600,700" rel="stylesheet">
  <style type="text/css">
    body {
      font-family: "Titillium Web", "Source Sans Pro", Apple SD Gothic Neo, Nanum Barun Gothic, Nanum Gothic, Verdana, Arial, Dotum, sans-serif;
      font-size: 1.2em;
      color: #343a40;
      background-color: #fff;
      -webkit-font-smoothing: antialiased;
      padding-top: 50px;
    }

    p {
      font-weight: 300;
    }

    .title {
      font-weight: 600;
      font-size: 1.7em;
    }

    td, .thin {
      font-weight: 300;
    }

    .seperator {
      border-bottom: 1px solid black;
      width: 500px;
    }

    .invoice-type {
      background-color: black;
      color: white;
      text-align: left;
    }

    .invert-color {
      background-color: black;
      color: white;
    }

    .col-half {
      width: 50%;
      display: inline-block;
      float: left;
      height: 175px;
      margin-top: 15px;
    }

    .bb-none {
      border-bottom: none !important;
    }

    .bt-none {
      border-top: none !important;
    }

    .bl-none {
      border-left: none !important;
    }

    .br-none {
      border-right: none !important;
    }

    .text-small {
      font-size: 0.75em;
    }

    .currency {
      float: left;
    }

    table {
      font-size: 0.9em;
    }

    .sep {
      margin: 15px 0px 30px 0px;
      width: 100%;
      height: 2px;
      background-color: #DEE2E6;
    }

    .bold {
      font-weight: 700;
    }

    .item-cell {
      border: none !important;
    }
  </style>
</head>
<body>
  <div class="row justify-content-center text-center mt-5">
    <div class="col-md-12 mb-4">
      <div class="title">[BUSINESS_NAME]</div>
      <div class="thin">[BUSINESS_ADDRESS]</div>
      <div class="thin">[BUSINESS_CITY_PROVINCE_COUNTRY]</div>
      <div class="thin">[BUSINESS_POSTAL_CODE]</div>
      <div class="thin text-small">[BUSINESS_PHONE]</div>
    </div>
  </div>
  <div class="row justify-content-center">
    <div class="col-sm-10 mb-4">
      <div class="text-justify text-uppercase thin pl-2 invoice-type mb-2">[INVOICE_TYPE]</div>
      <div class="col-half">
        <h4>BILL TO:</h4>
        <div class="thin">[CUSTOMER_NAME]</div>
        <div class="thin">[CUSTOMER_ADDRESS]</div>
        <div class="thin">[CUSTOMER_CITY_PROVINCE_COUNTRY]</div>
        <div class="thin">[CUSTOMER_POSTAL_CODE]</div>
      </div>
      <div class="col-half">
        <div><span class="thin">DATE:</span> [INVOICE_DATE]</div>
        <div><span class="thin text-uppercase">[INVOICE_TYPE] #:</span> [INVOICE_NUMBER]</div>
        <div><span class="thin">CUSTOMER ID:</span> [CUSTOMER_ID]</div>
      </div>
    </div>
    <div class="col-sm-10">
      <table class="table table-bordered">
        <tr>
          <th>Description</th>
          <th>Hours</th>
          <th>Pay Rate</th>
          <th>Amount (CAD)</th>
        </tr>
        [INVOICE_ITEMS]
        <tr>
          <td colspan="3" class="bb-none bl-none text-right">Subtotal</td>
          <td class="bb-none text-right"><span class="currency">$</span>[INVOICE_SUBTOTAL]</td>
        </tr>
        <tr>
          <td colspan="3" class="bb-none bt-none bl-none text-right">Tax</td>
          <td class="bb-none bt-none text-right"><span class="currency">$</span>-</td>
        </tr>
        <tr>
          <td colspan="3" class="bb-none bt-none bl-none text-right">Expenses</td>
          <td class="bb-none bt-none text-right"><span class="currency">$</span>-</td>
        </tr>
        <tr>
          <td colspan="3" class="bb-none bt-none bl-none text-right">Total</td>
          <td class="text-right invert-color"><span class="currency">$</span>[INVOICE_TOTAL]</td>
        </tr>
      </table>
    </div>
    <div class="col-sm-10 mt-2">
      <p class="text-center text-small">
        Please process all payments within <span class="bold">15 days</span> of receiving this invoice.
      </p>
      <ul>
        <li class="thin">Make all cheques payable to <span class="bold">Nafeu Nasir</span></li>
        <li class="thin">eTransfers and Paypal payments are also accepted, please send to  <span class="bold">nafeu.nasir@gmail.com</span></li>
      </ul>
    </div>
    <div class="col-sm-4">
      <div class="sep"></div>
    </div>
    <div class="col-sm-10">
      <p class="text-center text-small">
        If you have any questions about this invoice, please call +1(416)894-5354 or email <em>nafeu.nasir@gmail.com</em>
      </p>
    </div>
  </div>
</body>
</html>
"""

parser = argparse.ArgumentParser(description='Generate invoices.')
parser.add_argument('customer_id',
                    help="enter customer id to initialize invoice",
                    nargs='?',
                    const=0)
parser.add_argument("-l", "--list-customers",
                    help="list all customers",
                    action='store_true')
parser.add_argument("-b", "--build",
                    help="build a new pdf using the specified yaml file",
                    metavar='YAML_FILE',
                    nargs=1)
args = parser.parse_args()


def main():
    config = {}
    if (os.path.isfile(CONFIG_PATH)):
        with open(CONFIG_PATH) as raw_config:
            config = yaml.load(raw_config)
    else:
        create_yaml_file(CONFIG_PATH, DEFAULT_CONFIG)
        print("Missing config, please fill it in and try again.")
        open_file(CONFIG_PATH)
        exit()
    if args.list_customers:
        list_customers(config)
    elif args.build:
        data = {}
        if (os.path.isfile(args.build[0])):
            with open(args.build[0]) as raw_data:
                data = yaml.load(raw_data)
                build_pdf(config, data, args.build[0].replace(".yaml", ".pdf"))
        else:
            print("Invoice data file '%s' does not exist." % args.build[0])
    elif args.customer_id and len([(customer['id'] == args.customer_id) for customer in config['customers']]) > 0:
        init_new_invoice_data(config, get_customer_by_id(config['customers'], args.customer_id))
    else:
        parser.print_help(sys.stderr)


def list_customers(config):
    for customer in config['customers']:
        print("%s - %s" % (customer['id'], customer['name']))


def build_pdf(config, data, export_path):
    print("Generating...")
    processed_data = process_invoice_data(data)
    customer = get_customer_by_id(config['customers'], data['customer_id'])
    template = DEFAULT_TEMPLATE.replace("[BUSINESS_NAME]", config['name']) \
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
        .replace("[INVOICE_ITEMS]", get_invoice_items(processed_data)) \
        .replace("[INVOICE_SUBTOTAL]", str(get_invoice_subtotal(processed_data))) \
        .replace("[INVOICE_TOTAL]", str(get_invoice_total(processed_data)))
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
    file_name = "%s_-_%s_%s_-_%s.yaml" % (config['name'].replace(" ", "_"),
                                          customer['name'].replace(" ", "_"),
                                          data['invoice_type'].capitalize(),
                                          data['invoice_number'])
    create_yaml_file(file_name, data)
    open_file(file_name)


def create_yaml_file(path, data):
    with open(path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


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
    return now.strftime("%b %d, %Y")


def get_invoice_items(data):
    out = ""
    for item in data['items']:
        out += "<tr><td class='item-cell'>%s</td>" % process_item_desc(item['desc'])
        out += "<td class='text-center item-cell'>%s</td>" % item['hours']
        rate_label = "/hr"
        if "type" in item:
            rate_label = " (%s)" % item['type']
        out += "<td class='text-right item-cell'><span class='currency'>$</span>%s%s</td>" % (item['rate'], rate_label)
        out += "<td class='text-right item-cell'><span class='currency'>$</span>%s</td></tr>" % item['total']
    return out


def process_item_desc(desc):
    if isinstance(desc, list):
        out = ""
        for item in desc:
            if item[0].isupper():
                out += "%s</br>" % item
            else:
                out += "- %s</br>" % item
        return out
    return desc


def get_invoice_total(data):
    # TODO: Make more comprehensive
    return sum([item['total'] for item in data['items']])


def get_invoice_subtotal(data):
    return sum([item['total'] for item in data['items']])


def process_invoice_data(data):
    for item in data['items']:
        # TODO: Add more rate type options
        if "type" in item:
            item['total'] = item['rate']
        else:
            item['total'] = item['hours'] * item['rate']
    return data

if __name__ == '__main__':
    main()