const express = require('express');
const path = require('path');
const puppeteer = require('puppeteer-core');
const open = require('open');

const app = express();

const EXPORT_PATH = process.env.EXPORT_PATH || 'export.pdf'

app.set('view engine', 'ejs');
app.set("views", path.join(__dirname, "views"));

app.get('/', (req, res, next) => {
  res.render('invoice');
});

const server = app.listen(0, async () => {
  const port = server.address().port;

  console.log(`[ invoice-gen ] Building PDF...`);

  const browser = await puppeteer.launch();
  const page    = await browser.newPage();

  const url = `http://localhost:${port}`;

  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.emulateMediaType('screen');

  const pdf = await page.pdf({
    path: EXPORT_PATH,
    margin: { top: '100px', right: '50px', bottom: '100px', left: '50px' },
    printBackground: true,
    format: 'A4',
  });

  await browser.close();

  console.log(`Complete.`);

  open(EXPORT_PATH);

  process.exit(0);
});
