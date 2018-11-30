import pdfkit

def main():
  config = {
    "name": "Nafeu Nasir Media Solutions",
    "address": "EXAMPLE ADDRESS",
    "city_province_country": "Toronto, Ontario, Canada",
    "postal_code": "??????",
    "phone": "+1(111)-111-1111",
    "invoice_type": "invoice",
  }
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
    print("Complete.")

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