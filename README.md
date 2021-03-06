# Invoice Generator

Basic invoice generator for quick PDF invoices/quotes.

### Requirements

- Python 3
- Homebrew

### Setup / Installation (MAC)

```
git clone https://github.com/nafeu/invoice-gen.git
cd invoice-gen
pip install -r requirements.txt
brew install Caskroom/cask/wkhtmltopdf
```

### Usage

*Use `python3` in place of `python` as required, for now I am assuming version 3 is the default*

```
touch config.yaml
```

Fill your `config.yaml` with the following information:

```
name: [BUSINESS_NAME]
address: [BUSINESS_ADDRESS]
city_province_country: [BUSINESS_CITY_PROVINCE_COUNTRY]
postal_code: [BUSINESS_POSTAL_CODE]
abrv: [BUSINESS_ABBREVIATION]
phone: BUSINESS_PHONE
customers:
- id: 1
  name: [CUSTOMER_1_NAME]
  address: [CUSTOMER_1_ADDRESS]
  city_province_country: [CUSTOMER_1_CITY_PROVINCE_COUNTRY]
  postal_code: [CUSTOMER_1_POSTAL_CODE]
  phone: [CUSTOMER_1_PHONE]
- id: 2
  name: [CUSTOMER_2_NAME]
  address: [CUSTOMER_2_ADDRESS]
  city_province_country: [CUSTOMER_2_CITY_PROVINCE_COUNTRY]
  postal_code: [CUSTOMER_2_POSTAL_CODE]
  phone: [CUSTOMER_2_PHONE]
- ...
```

Then use `python invoice-gen.py [CUSTOMER_ID]` to generate an invoice data file like the following and fill it information:

```
customer_id: [CUSTOMER_ID]
invoice_date: [AUTOGENERATED_INVOICE_DATE]
invoice_number: [AUTOGENERATED_INVOICE_NUMBER]
invoice_type: invoice
items:
- desc:
  - Main work item
  - small task
  - another task
  hours: [HOURS]
  rate: [RATE]
- desc: Less complex task
  hours: [HOURS]
  rate: [RATE]
```

You can change `invoice_type` value to `quote` if you are generating a quote instead. Then build the final invoice/quote as follows:

```
python invoice-gen.py -b [INVOICE_DATA_YAML_FILE_PATH]
```

Use the exported pdf and profit. For additional help use `python invoice-gen.py -h`. I would also recommend adding the following alias to your zsh or bash rc:

```
alias invoice="python [PATH_TO_PROJECT_DIR]/invoice-gen.py"
```

If you are using **Python 2** as default:

```
alias invoice="python3 [PATH_TO_PROJECT_DIR]/invoice-gen.py"
```

### Author

Nafeu Nasir (nafeu.com)

### License

MIT