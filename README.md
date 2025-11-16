# WebsiteDorkerPro 🔍

**Website Reconnaissance Toolkit for Bug Hunters and Pentesters**

[![PyPI version](https://img.shields.io/pypi/v/website-dorker-pro.svg)](https://pypi.org/project/website-dorker-pro/)
[![Python Versions](https://img.shields.io/pypi/pyversions/website-dorker-pro.svg)](https://pypi.org/project/website-dorker-pro/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive reconnaissance tool for bug bounty hunters, penetration testers, and security researchers. WebsiteDorkerPro provides a powerful GUI and CLI interface for performing Google dorking and external reconnaissance.

## Features

- 🕵️‍♂️ **Comprehensive Reconnaissance**: Subdomains, certificates, DNS, headers
- 📁 **File Discovery**: Configs, databases, backups, sensitive files  
- 🔧 **Technology Detection**: WordPress, PHP, frameworks, CMS detection
- 🛡️ **Vulnerability Scanning**: SQL errors, XSS, shells, redirects
- 🔐 **Sensitive Data Exposure**: API keys, user data, payment info
- 🌐 **External Recon**: GitHub, Pastebin, social media
- ☁️ **Cloud & Infrastructure**: S3, Azure, Shodan, Censys
- ⚡ **Custom Tools**: Custom dorks, quick scans, utilities

![image](banner.png)

## Installation

### From PyPI
```bash
sudo python3 -m pip install website-dorker-pro --break-system-packages
```

### From Source
```bash

git clone https://github.com/ZishanAdThandar/WebsiteDorkerPro.git
cd WebsiteDorkerPro
pip install -e .
```
## Usage

### GUI Interface

```bash

websitedorkerpro --gui
# or
wdp --gui
```

### CLI Interface
```bash

# Quick reconnaissance scan
websitedorkerpro example.com --quick-scan

# Specific dork category
websitedorkerpro example.com --category subdomains

# Custom dork
websitedorkerpro example.com --dork "site:{domain} ext:pdf"

# List available categories

websitedorkerpro --list-categories
```

### Python API

```python

from website_dorker_pro import WebsiteDorkerPro
import tkinter as tk

root = tk.Tk()
app = WebsiteDorkerPro(root)
app.run()

Available Dork Categories

    subdomains - Find subdomains

    files - Open directories and files

    configs - Configuration files

    databases - Database files and dumps

    logs - Application log files

    backups - Backup and old files

    login - Login and authentication pages

    docs - Documents (PDF, DOC, XLS, etc)

    wordpress - WordPress-specific reconnaissance

    github - GitHub code search

    pastebin - Pastebin leaks
```


## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features.
License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Zishan Ahamed Thandar

  -  Portfolio: [ZishanAdThandar.github.io](https:/zishanadthandar.github.io)

  -  GitHub: [@ZishanAdThandar](https://github.com/ZishanAdThandar/)

## Disclaimer

This tool is intended for educational purposes and legitimate security testing only. Always ensure you have proper authorization before testing any systems. The developers are not responsible for any misuse of this tool.

