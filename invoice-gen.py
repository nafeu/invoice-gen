import pdfkit
import json
import subprocess
import argparse
import os.path

CONFIG_PATH = "config.json"
DEFAULT_CONFIG = {
  "name": "[BUSINESS_NAME]",
  "address": "[BUSINESS_ADDRESS]",
  "city_province_country": "[BUSINESS_CITY_PROVINCE_COUNTRY]",
  "postal_code": "[BUSINESS_POSTAL_CODE]",
  "phone": "[BUSINESS_PHONE]",
  "email": "[BUSINESS_EMAIL]",
  "invoice_type": "invoice",
  "clients": [
    {
      "id": 1,
      "name": "[CLIENT_NAME]",
      "address": "[CLIENT_ADDRESS]",
      "postal": "[CLIENT_POSTAL]",
      "phone": "[CLIENT_PHONE]"
    }
  ]
}

parser = argparse.ArgumentParser()
parser.add_argument("clients", nargs='?')
parser.add_argument("-b", "--build",
                    help="build a new pdf",
                    metavar='JSON',
                    nargs=1)

args = parser.parse_args()

def main():
  config = {}
  # if (os.path.isfile(args.build[0])):
  #   with open(args.build[0]) as raw_config:
  #     config = json.load(raw_config)

  if (os.path.isfile(CONFIG_PATH)):
    with open(CONFIG_PATH) as raw_config:
      config = json.load(raw_config)
  else:
    with open(CONFIG_PATH, 'w') as file:
      json.dump(DEFAULT_CONFIG, file, indent=2)
    print("Missing config, please fill it in and try again.")
    subprocess.check_call(["open", CONFIG_PATH])
    exit()

  if (args.clients):
    for client in config['clients']:
      print("%s - %s" % (client['id'], client['name']))
  elif (args.build):
    with open("templates/index.html", "r") as file:
      print("Generating...")
      template = file.read()
      template = template.replace("[BUSINESS_NAME]", config['name']) \
                         .replace("[BUSINESS_ADDRESS]", config['address']) \
                         .replace("[BUSINESS_CITY_PROVINCE_COUNTRY]", config['city_province_country']) \
                         .replace("[BUSINESS_POSTAL_CODE]", config['postal_code']) \
                         .replace("[BUSINESS_PHONE]", config['phone']) \
                         .replace("[INVOICE_TYPE]", config['invoice_type'], 2) \
                         .replace("[INVOICE_ITEMS]", getInvoiceItems())
      pdfkit.from_string(template, 'export.pdf')
      subprocess.check_call(["open", "-a", "Preview.app", "export.pdf"])
      print("Complete.")
  else:
    print(args)

def getInvoiceItems():
    items = [
      {
        "desc": "Completed such and such work and did this and that",
        "hours": 40,
        "rate": 25,
        "total": 1000.00
      },
      {
        "desc": "Did some stuff here and there",
        "hours": 40,
        "rate": 25,
        "total": 1000.00
      },
      {
        "desc": "Did some other stuff here and there",
        "hours": 40,
        "rate": 25,
        "total": 1000.00
      }
    ]
    out = ""
    for item in items:
      out += "<tr><td>%s</td>" % item['desc']
      out += "<td class='text-right'>%s</td>" % item['hours']
      out += "<td class='text-right'><span class='currency'>$</span>%s</td>" % item['rate']
      out += "<td class='text-right'><span class='currency'>$</span>%s</td></tr>" % item['total']
    return out

if __name__ == '__main__':
  main()