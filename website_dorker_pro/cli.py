#!/usr/bin/env python3
"""
Command Line Interface for WebsiteDorkerPro
"""

import argparse
import webbrowser
import urllib.parse
import sys

try:
    from .core import passive_recon
except ImportError:
    try:
        from core import passive_recon
    except ImportError:
        passive_recon = None

class WebsiteDorkerProCLI:
    """Command Line Interface for WebsiteDorkerPro"""
    
    def __init__(self):
        self.dork_categories = {
            'subdomains': 'site:*.{domain}',
            'files': 'site:{domain} intitle:index.of',
            'configs': 'site:{domain} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini',
            'databases': 'site:{domain} ext:sql | ext:dbf | ext:mdb',
            'logs': 'site:{domain} ext:log',
            'backups': 'site:{domain} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup',
            'login': 'site:{domain} inurl:login | inurl:signin | intitle:Login | intitle: signin | inurl:auth',
            'docs': 'site:{domain} ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv',
            'wordpress': 'site:{domain} inurl:wp- | inurl:wp-content | inurl:plugins | inurl:uploads | inurl:themes | inurl:download',
            'github': 'site:github.com "{domain}"',
            'pastebin': 'site:pastebin.com "{domain}"'
        }
    
    def search(self, domain, category, custom_dork=None):
        """Perform a dork search"""
        if custom_dork:
            dork = custom_dork.format(domain=domain)
        else:
            dork = self.dork_categories.get(category, '').format(domain=domain)
        
        if not dork:
            print(f"❌ Unknown category: {category}")
            return False
        
        url = f"https://www.google.com/search?q={urllib.parse.quote(dork)}"
        print(f"🔍 Searching: {dork}")
        print(f"🌐 Opening: {url}")
        
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"❌ Error opening browser: {e}")
            return False
    
    def list_categories(self):
        """List available dork categories"""
        print("Available dork categories:")
        for category in self.dork_categories:
            print(f"  - {category}")
    
    def quick_scan(self, domain):
        """Perform a quick reconnaissance scan"""
        quick_categories = ['subdomains', 'files', 'configs', 'login', 'backups']
        print(f"🚀 Starting quick reconnaissance for: {domain}")
        
        for category in quick_categories:
            self.search(domain, category)
        
        print("✅ Quick scan completed!")
    
    def live_recon(self, domain):
        """
        Run the dependency-free live reconnaissance sweep (core.py) and
        return the plain-text report. Prints progress to stdout.
        """
        if passive_recon is None:
            return "❌ Recon engine unavailable (core.py missing)."
        print(f"🛰️ Live reconnaissance for: {domain}")
        report = passive_recon(domain)
        print(report)
        return report

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="WebsiteDorkerPro - Website Reconnaissance Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  websitedorkerpro example.com --category subdomains
  websitedorkerpro example.com --quick-scan
  websitedorkerpro --list-categories
  websitedorkerpro --gui
        """
    )
    
    parser.add_argument('domain', nargs='?', help='Target domain to scan')
    parser.add_argument('-c', '--category', help='Dork category to use')
    parser.add_argument('-d', '--dork', help='Custom dork string (use {domain} as placeholder)')
    parser.add_argument('-q', '--quick-scan', action='store_true', help='Perform quick reconnaissance scan')
    parser.add_argument('-r', '--recon', action='store_true',
                        help='Run live dependency-free recon (DNS, headers, robots, subdomains, fuzz)')
    parser.add_argument('-e', '--export', metavar='FILE',
                        help='Save the recon report to a text file')
    parser.add_argument('-l', '--list-categories', action='store_true', help='List available dork categories')
    parser.add_argument('-g', '--gui', action='store_true', help='Launch GUI interface')
    
    args = parser.parse_args()
    
    cli = WebsiteDorkerProCLI()
    
    if args.list_categories:
        cli.list_categories()
        return
    
    if args.recon:
        if not args.domain:
            parser.print_help()
            return
        report = cli.live_recon(args.domain)
        if args.export:
            try:
                with open(args.export, 'w', encoding='utf-8') as fh:
                    fh.write(report)
                print(f"\n📁 Report saved to: {args.export}")
            except Exception as e:
                print(f"❌ Could not write report: {e}")
        return
    
    if args.gui:
        try:
            from .main import WebsiteDorkerPro, HAS_TKINTER
        except ImportError:
            # Fallback for direct execution
            from main import WebsiteDorkerPro, HAS_TKINTER
        if not HAS_TKINTER:
            print("❌ tkinter is not available. Install it via your system package manager (e.g. 'sudo apt install python3-tk').")
            sys.exit(1)
        app = WebsiteDorkerPro()
        app.run()
        return
    
    if not args.domain:
        parser.print_help()
        return
    
    if args.quick_scan:
        cli.quick_scan(args.domain)
    elif args.category:
        cli.search(args.domain, args.category, args.dork)
    elif args.dork:
        cli.search(args.domain, None, args.dork)
    else:
        print("Please specify a category or use --quick-scan")
        parser.print_help()

if __name__ == "__main__":
    main()