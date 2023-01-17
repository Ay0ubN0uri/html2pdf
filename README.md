<h3 align="center">Html2pdf</h3>
<div align="center">
<p align="center">
Gui application for converting html to pdf.
</p>
<a href="https://github.com/Ay0ubN0uri/html2pdf/issues">Report Issue</a>
<span>|</span>
<a href="https://github.com/Ay0ubN0uri/html2pdf/issues">Request Feature</a>
</div>

## Usage
---

![html2pdf image](https://github.com/Ay0ubN0uri/html2pdf/blob/master/html2pdf.png)

## Features:
---
- Convert multiple html files to pdf.
- Convert multiple urls to pdf.

## Installation / How to use:
---
1. Clone the repository:
```bash
	git clone https://github.com/Ay0ubN0uri/html2pdf.git
```
3. Install Requirements:
```bash
	pip install -r requirements.txt
```
3. Install wkhtmltopdf:
	- Debian/Ubuntu:
		```bash
		sudo apt-get install wkhtmltopdf
		```
	- macOS:
		```bash
		brew install homebrew/cask/wkhtmltopdf
		```
	- Windows:
			Install the release from [here](https://github.com/Ay0ubN0uri/html2pdf/releases/tag/V0.1.0)

**Warning!** Version in debian/ubuntu repos have reduced functionality (because it compiled without the wkhtmltopdf QT patches), such as adding outlines, headers, footers, TOC etc. To use this options you should install static binary from [wkhtmltopdf](http://wkhtmltopdf.org/) site or you can use this [script](https://github.com/JazzCore/python-pdfkit/blob/master/ci/before-script.sh) (written for CI servers with Ubuntu 18.04 Bionic, but it could work on other Ubuntu/Debian versions).

## Contact
---
- LinkedIn: [ayoub nouri](https://www.linkedin.com/in/ayoub-nouri-73532a244/)

- Email: ayoub.nouri105@gmail.com