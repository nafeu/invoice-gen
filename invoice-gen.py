import pdfkit

def main():
  print("Generating...")
  pdfkit.from_file('templates/header.html', 'export.pdf')
  print("Complete.")

if __name__ == '__main__':
  main()