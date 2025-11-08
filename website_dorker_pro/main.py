import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import urllib.parse
from datetime import datetime

class WebsiteDorkerPro:
    """
    Website Reconnaissance Toolkit for Bug Hunters and Pentesters
    
    A comprehensive GUI tool for bug bounty reconnaissance using Google dorks
    and external reconnaissance techniques.
    """
    
    def __init__(self, root=None):
        """
        Initialize the WebsiteDorkerPro application
        
        Args:
            root: Tkinter root window (creates new if None)
        """
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the main GUI interface"""
        self.root.title("WebsiteDorkerPro - Website Reconnaissance Toolkit")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0d1117")
        
        # Style configuration for dark theme
        self.setup_styles()
        
        # Header
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(header_frame, text="🔍 WebsiteDorkerPro", 
                 font=("Consolas", 18, "bold"), 
                 foreground="#ff6b35",
                 style="Header.TLabel").pack(side=tk.LEFT)
        
        ttk.Label(header_frame, text="Website Reconnaissance Toolkit", 
                 font=("Consolas", 10),
                 foreground="#8b949e",
                 style="Header.TLabel").pack(side=tk.LEFT, padx=(10, 0))
        
        # Domain input frame
        input_frame = ttk.Frame(self.root, style="Main.TFrame")
        input_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(input_frame, text="Target Domain:", 
                 style="Custom.TLabel").pack(side=tk.LEFT)
        
        self.domain_entry = ttk.Entry(input_frame, width=40, font=("Consolas", 10))
        self.domain_entry.pack(side=tk.LEFT, padx=10)
        self.domain_entry.bind("<Return>", lambda e: self.quick_recon())
        
        ttk.Button(input_frame, text="Quick Recon", 
                  command=self.quick_recon,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Clear", 
                  command=self.clear_domain,
                  style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        
        # Tabbed interface
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_recon_tab(notebook)
        self.create_files_tab(notebook)
        self.create_tech_tab(notebook)
        self.create_vuln_tab(notebook)
        self.create_sensitive_tab(notebook)
        self.create_external_tab(notebook)
        self.create_cloud_tab(notebook)
        self.create_tools_tab(notebook)
        
        # Status bar
        self.status_var = tk.StringVar(value="🚀 Ready - Enter target domain to begin reconnaissance")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, 
                              style="Status.TLabel")
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=5)
        
        # Footer
        footer_frame = ttk.Frame(self.root, style="Footer.TFrame")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=5)
        
        ttk.Label(footer_frame, text="Developed by ZishanAdThandar | ", 
                 style="Footer.TLabel").pack(side=tk.LEFT)
        
        portfolio_link = ttk.Label(footer_frame, text="Portfolio", cursor="hand2", 
                                 foreground="#ff6b35", style="Footer.TLabel")
        portfolio_link.pack(side=tk.LEFT)
        portfolio_link.bind("<Button-1>", lambda e: webbrowser.open("https://ZishanAdThandar.github.io"))
        
        ttk.Label(footer_frame, text=" | ", style="Footer.TLabel").pack(side=tk.LEFT)
        
        github_link = ttk.Label(footer_frame, text="GitHub", cursor="hand2",
                              foreground="#ff6b35", style="Footer.TLabel")
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/ZishanAdThandar"))
    
    def setup_styles(self):
        """Configure tkinter styles for dark theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for GitHub-like dark theme
        bg_color = "#0d1117"
        card_bg = "#161b22"
        border_color = "#30363d"
        accent_color = "#ff6b35"
        text_color = "#f0f6fc"
        muted_text = "#8b949e"
        
        style.configure('Header.TFrame', background=bg_color)
        style.configure('Header.TLabel', background=bg_color, foreground=text_color)
        style.configure('Main.TFrame', background=bg_color)
        style.configure('Custom.TLabel', background=bg_color, foreground=text_color)
        style.configure('Footer.TFrame', background=bg_color)
        style.configure('Footer.TLabel', background=bg_color, foreground=muted_text)
        style.configure('Status.TLabel', background=card_bg, foreground=text_color)
        style.configure('Card.TFrame', background=card_bg, relief='raised', borderwidth=1)
        style.configure('Card.TLabelframe', background=card_bg, foreground=accent_color)
        style.configure('Card.TLabelframe.Label', background=card_bg, foreground=accent_color)
        
        style.configure('Accent.TButton', background=accent_color, foreground='white')
        style.configure('Secondary.TButton', background=border_color, foreground=text_color)
        
        style.map('Accent.TButton',
                 background=[('active', '#e55a2b'), ('pressed', '#cc4a24')])
        style.map('Secondary.TButton',
                 background=[('active', '#3d444d'), ('pressed', '#484f58')])

    def create_section(self, parent, title, buttons, columns=2):
        """Create a section with title and buttons in grid layout"""
        section_frame = ttk.LabelFrame(parent, text=title, style="Card.TLabelframe", padding=10)
        section_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for i, (text, command, tooltip) in enumerate(buttons):
            row = i // columns
            col = (i % columns) * 2
            btn = ttk.Button(section_frame, text=text, command=command, width=28)
            btn.grid(row=row, column=col, padx=5, pady=3, sticky=tk.W)
            if tooltip:
                self.create_tooltip(btn, tooltip)

    def create_tooltip(self, widget, text):
        """Create tooltip for buttons"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = ttk.Label(tooltip, text=text, background="#ffffe0", 
                            relief='solid', borderwidth=1, padding=5)
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def create_recon_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="🔍 Reconnaissance")
        
        recon_frame = ttk.Frame(tab, style="Main.TFrame")
        recon_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("🌐 Subdomains Discovery", self.subdomains_single, "Find subdomains (*.domain.com)"),
            ("🌍 Deep Subdomains", self.subdomains_double, "Find deeper subdomains (*.*.domain.com)"),
            ("📜 SSL Certificates", self.certificate_search, "Search SSL certificates on crt.sh"),
            ("🕵️‍♂️ Wayback Machine", self.wayback_machine, "Check historical site data"),
            ("🔍 DNS Reconnaissance", self.dns_recon, "DNS information and reverse IP lookup"),
            ("📊 Security Headers", self.security_headers, "Analyze security headers"),
        ]
        self.create_section(recon_frame, "Initial Reconnaissance", buttons, columns=2)

    def create_files_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="📁 File Discovery")
        
        files_frame = ttk.Frame(tab, style="Main.TFrame")
        files_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("📂 Open Directories", self.open_directories, "Find open directory listings"),
            ("⚙️ Configuration Files", self.config_files, "Find configuration files"),
            ("🗄️ Database Files", self.database_files, "Find database files and dumps"),
            ("📊 Log Files", self.log_files, "Find application log files"),
            ("💾 Backup Files", self.backup_files, "Find backup and old files"),
            ("📄 Documents", self.documents, "Find documents (PDF, DOC, XLS, etc)"),
        ]
        self.create_section(files_frame, "File Discovery", buttons, columns=2)

    def create_tech_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="🔧 Technology")
        
        tech_frame = ttk.Frame(tab, style="Main.TFrame")
        tech_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("🚀 WordPress Scan", self.wordpress, "WordPress-specific reconnaissance"),
            ("🐘 PHP Info Pages", self.php_info, "Find PHP info pages"),
            ("⚡ Apache Configs", self.apache_config, "Find Apache configuration files"),
            ("🔧 Environment Files", self.env_files, "Find environment configuration files"),
            ("🐍 Django Applications", self.django_debug, "Find Django debug mode enabled"),
        ]
        self.create_section(tech_frame, "Technology Detection", buttons, columns=2)

    def create_vuln_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="🛡️ Vulnerabilities")
        
        vuln_frame = ttk.Frame(tab, style="Main.TFrame")
        vuln_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("🚨 SQL Errors", self.sql_errors, "Find SQL error messages"),
            ("🔐 Login Pages", self.login_pages, "Find login and authentication pages"),
            ("🔄 Open Redirects", self.redirects, "Find potential open redirects"),
            ("🏴‍☠️ Web Shells", self.shells_backdoors, "Find web shells and backdoors"),
            ("📡 Crossdomain Policy", self.crossdomain_xml, "Check crossdomain.xml policies"),
        ]
        self.create_section(vuln_frame, "Vulnerability Scanning", buttons, columns=2)

    def create_sensitive_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="🔐 Sensitive Data")
        
        sensitive_frame = ttk.Frame(tab, style="Main.TFrame")
        sensitive_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("🔑 API Keys & Tokens", self.api_keys, "Find exposed API keys and tokens"),
            ("📧 Email Lists", self.email_lists, "Find email lists and databases"),
            ("👥 User Information", self.exposed_users, "Find exposed user information"),
            ("💰 Payment Data", self.payment_info, "Find payment-related files"),
        ]
        self.create_section(sensitive_frame, "Sensitive Data Exposure", buttons, columns=2)

    def create_external_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="🌐 External Recon")
        
        external_frame = ttk.Frame(tab, style="Main.TFrame")
        external_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("💾 GitHub Search", self.github_search, "Search GitHub for exposed code"),
            ("📋 Pastebin Leaks", self.pastebin_search, "Search Pastebin for leaks"),
            ("💼 LinkedIn Employees", self.linkedin_employees, "Find company employees"),
            ("🗣️ Reddit Mentions", self.reddit_search, "Search Reddit for mentions"),
        ]
        self.create_section(external_frame, "External Reconnaissance", buttons, columns=2)

    def create_cloud_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="☁️ Cloud & Infra")
        
        cloud_frame = ttk.Frame(tab, style="Main.TFrame")
        cloud_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("☁️ AWS S3 Buckets", self.s3_buckets, "Find exposed AWS S3 buckets"),
            ("🌊 DigitalOcean Spaces", self.digitalocean_spaces, "Find DigitalOcean Spaces"),
            ("🚢 Azure Blob Storage", self.azure_blobs, "Find Azure storage blobs"),
            ("🔍 Shodan Search", self.shodan_search, "Search Shodan for exposed services"),
        ]
        self.create_section(cloud_frame, "Cloud & Infrastructure", buttons, columns=2)

    def create_tools_tab(self, notebook):
        tab = ttk.Frame(notebook, style="Main.TFrame")
        notebook.add(tab, text="⚡ Tools")
        
        tools_frame = ttk.Frame(tab, style="Main.TFrame")
        tools_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ("🎯 Custom Dork Search", self.custom_dork_search, "Search with custom Google dork"),
            ("🚀 Quick Recon Scan", self.quick_scan, "Run multiple common searches"),
            ("📊 CMS Detection", self.cms_detection, "Detect CMS and technologies"),
        ]
        self.create_section(tools_frame, "Custom Tools", buttons, columns=2)

    # === Utility Methods ===
    def get_domain(self):
        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showwarning("Input Required", "Please enter a target domain")
            return None
        return domain

    def open_url(self, url):
        try:
            webbrowser.open(url)
            self.status_var.set(f"🔍 Search opened: {url[:80]}...")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {str(e)}")

    def log_search(self, search_type):
        domain = self.domain_entry.get()
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(f"✅ [{timestamp}] {search_type} for {domain}")

    # === RECONNAISSANCE METHODS ===
    def subdomains_single(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:*.{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("Subdomain discovery")

    def subdomains_double(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:*.*.{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("Deep subdomain discovery")

    def certificate_search(self):
        if domain := self.get_domain():
            url = f"https://crt.sh/?q={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("SSL certificate search")

    def wayback_machine(self):
        if domain := self.get_domain():
            url = f"https://web.archive.org/web/*/{urllib.parse.quote(domain)}/*"
            self.open_url(url)
            self.log_search("Wayback Machine search")

    def dns_recon(self):
        if domain := self.get_domain():
            url = f"https://viewdns.info/reverseip/?host={urllib.parse.quote(domain)}&t=1"
            self.open_url(url)
            self.log_search("DNS reconnaissance")

    def security_headers(self):
        if domain := self.get_domain():
            url = f"https://securityheaders.com/?q={urllib.parse.quote(domain)}&followRedirects=on"
            self.open_url(url)
            self.log_search("Security headers check")

    # === FILE DISCOVERY METHODS ===
    def open_directories(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intitle:index.of"
            self.open_url(url)
            self.log_search("Open directories")

    def config_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:xml+|+ext:conf+|+ext:cnf+|+ext:reg+|+ext:inf+|+ext:rdp+|+ext:cfg+|+ext:txt+|+ext:ora+|+ext:ini+|+ext:env"
            self.open_url(url)
            self.log_search("Configuration files")

    def database_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:sql+|+ext:dbf+|+ext:mdb+|+ext:db+|+ext:sqlite+|+ext:dump"
            self.open_url(url)
            self.log_search("Database files")

    def log_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:log+|+ext:logs"
            self.open_url(url)
            self.log_search("Log files")

    def backup_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:bkf+|+ext:bkp+|+ext:bak+|+ext:old+|+ext:backup+|+ext:tar.gz+|+ext:tgz+|+ext:zip"
            self.open_url(url)
            self.log_search("Backup files")

    def documents(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:doc+|+ext:docx+|+ext:odt+|+ext:pdf+|+ext:rtf+|+ext:sxw+|+ext:psw+|+ext:ppt+|+ext:pptx+|+ext:pps+|+ext:csv+|+ext:xls+|+ext:xlsx"
            self.open_url(url)
            self.log_search("Documents")

    # === TECHNOLOGY DETECTION METHODS ===
    def wordpress(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:wp-+|+inurl:wp-content+|+inurl:plugins+|+inurl:uploads+|+inurl:themes"
            self.open_url(url)
            self.log_search("WordPress reconnaissance")

    def php_info(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:php+intitle:phpinfo+%22published+by+the+PHP+Group%22"
            self.open_url(url)
            self.log_search("PHP info pages")

    def apache_config(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+filetype:config+%22apache%22"
            self.open_url(url)
            self.log_search("Apache config files")

    def env_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:env+|+inurl:.env+%22API%22+%22KEY%22"
            self.open_url(url)
            self.log_search("Environment files")

    def django_debug(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intext:%22DEBUG+%3D+True%22+|+intext:%22settings.DEBUG%22"
            self.open_url(url)
            self.log_search("Django debug mode")

    # === VULNERABILITY SCANNING METHODS ===
    def sql_errors(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intext:%22sql+syntax+near%22+|+intext:%22syntax+error+has+occurred%22+|+intext:%22Warning:+mysql_connect()%22"
            self.open_url(url)
            self.log_search("SQL errors")

    def login_pages(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:login+|+inurl:signin+|+intitle:Login+|+intitle:signin+|+inurl:auth"
            self.open_url(url)
            self.log_search("Login pages")

    def redirects(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:redir+|+inurl:url+|+inurl:redirect+|+inurl:return+|+inurl:src=http"
            self.open_url(url)
            self.log_search("Open redirects")

    def shells_backdoors(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:shell+|+inurl:backdoor+|+inurl:wso+|+inurl:c99+|+inurl:r57"
            self.open_url(url)
            self.log_search("Web shells")

    def crossdomain_xml(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q={urllib.parse.quote(domain)}/crossdomain.xml"
            self.open_url(url)
            self.log_search("Crossdomain policy")

    # === SENSITIVE DATA METHODS ===
    def api_keys(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22api_key%22+|+%22api+key%22+|+%22secret_key%22+|+%22password%22+filetype:env"
            self.open_url(url)
            self.log_search("API keys")

    def email_lists(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:csv+|+ext:xls+|+ext:xlsx+%22email%22+%22password%22"
            self.open_url(url)
            self.log_search("Email lists")

    def exposed_users(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intitle:%22index+of%22+%22users%22+|+inurl:%22user+profiles%22"
            self.open_url(url)
            self.log_search("Exposed users")

    def payment_info(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22payment%22+|+%22credit+card%22+|+%22paypal%22+filetype:csv"
            self.open_url(url)
            self.log_search("Payment information")

    # === EXTERNAL RECON METHODS ===
    def github_search(self):
        if domain := self.get_domain():
            url = f"https://github.com/search?q=%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_search("GitHub search")

    def pastebin_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:pastebin.com+{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("Pastebin search")

    def linkedin_employees(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:linkedin.com+employees+{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("LinkedIn employees")

    def reddit_search(self):
        if domain := self.get_domain():
            url = f"https://www.reddit.com/search/?q={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("Reddit search")

    # === CLOUD INFRASTRUCTURE METHODS ===
    def s3_buckets(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:.s3.amazonaws.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_search("S3 buckets")

    def digitalocean_spaces(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:digitaloceanspaces.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_search("DigitalOcean Spaces")

    def azure_blobs(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:blob.core.windows.net+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_search("Azure Blobs")

    def shodan_search(self):
        if domain := self.get_domain():
            url = f"https://www.shodan.io/search?query={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("Shodan search")

    # === CUSTOM TOOLS METHODS ===
    def custom_dork_search(self):
        if domain := self.get_domain():
            dork = simpledialog.askstring("Custom Dork", "Enter your Google dork:")
            if dork:
                url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+{urllib.parse.quote(dork)}"
                self.open_url(url)
                self.log_search("Custom dork search")

    def quick_scan(self):
        if domain := self.get_domain():
            # Run multiple common searches
            searches = [
                self.open_directories,
                self.config_files,
                self.login_pages,
                self.backup_files,
                self.php_info
            ]
            for search in searches:
                search()
            self.status_var.set("✅ Quick scan completed - multiple searches opened")

    def cms_detection(self):
        if domain := self.get_domain():
            url = f"https://whatcms.org/?s={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_search("CMS detection")

    def quick_recon(self):
        if domain := self.get_domain():
            self.quick_scan()

    def clear_domain(self):
        self.domain_entry.delete(0, tk.END)
        self.status_var.set("🔄 Domain cleared - Enter new target domain")

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

def main():
    """Main entry point for the GUI application"""
    app = WebsiteDorkerPro()
    app.run()

if __name__ == "__main__":
    main()