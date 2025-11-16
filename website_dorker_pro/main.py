import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import urllib.parse
import re
from datetime import datetime

class WebsiteDorkerPro:
    """
    Website Reconnaissance Toolkit for Bug Hunters and Pentesters
    """
    
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
            
        self.setup_gui()
    
    def extract_domain(self, url):
        """Extract domain name from URL with http/https"""
        # Remove http:// or https://
        domain = re.sub(r'^https?://', '', url)
        # Remove www.
        domain = re.sub(r'^www\.', '', domain)
        # Remove path and query parameters
        domain = re.sub(r'[/?#].*$', '', domain)
        # Remove trailing slash
        domain = domain.rstrip('/')
        return domain
    
    def setup_gui(self):
        """Setup the main GUI interface with comfortable hacker theme"""
        self.root.title("WebsiteDorkerPro - Reconnaissance Toolkit")
        self.root.geometry("1150x650")  # Reduced height
        
        # Comfortable hacker color scheme - Softer greens on dark gray
        self.bg_color = "#0a0a0a"        # Soft black
        self.card_bg = "#1a1a1a"         # Dark gray cards
        self.fg_color = "#90ee90"        # Soft green - easier on eyes
        self.accent_color = "#32cd32"    # Lime green for accents
        self.highlight_color = "#98fb98" # Pale green for highlights
        self.border_color = "#2a2a2a"    # Subtle borders
        self.button_bg = "#2a2a2a"       # Button background
        
        # Configure the main window
        self.root.configure(bg=self.bg_color)
        
        # Style configuration for comfortable theme
        self.setup_styles()
        
        # Header with clean design
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=12)
        
        # Clean header without ASCII art
        title_label = ttk.Label(header_frame, 
                               text="WebsiteDorkerPro", 
                               font=("Segoe UI", 20, "bold"), 
                               foreground=self.accent_color,
                               style="Header.TLabel")
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                  text="Professional Reconnaissance Toolkit", 
                                  font=("Segoe UI", 11),
                                  foreground=self.fg_color,
                                  style="Header.TLabel")
        subtitle_label.pack(pady=(2, 0))
        
        # Target input section
        input_frame = ttk.Frame(self.root, style="Main.TFrame")
        input_frame.pack(fill=tk.X, padx=20, pady=12)
        
        # Input label
        input_label = ttk.Label(input_frame, 
                               text="Target Domain:", 
                               font=("Segoe UI", 10, "bold"),
                               style="Custom.TLabel")
        input_label.pack(side=tk.LEFT)
        
        # Input field with comfortable styling and placeholder
        self.domain_entry = tk.Entry(input_frame, 
                                    width=45, 
                                    font=("Segoe UI", 10),
                                    bg=self.card_bg, 
                                    fg=self.fg_color,
                                    insertbackground=self.fg_color,
                                    relief="flat",
                                    bd=2,
                                    highlightbackground=self.border_color,
                                    highlightcolor=self.accent_color,
                                    highlightthickness=1)
        self.domain_entry.pack(side=tk.LEFT, padx=12, pady=6)
        self.domain_entry.insert(0, "example.com or https://example.com")
        self.domain_entry.bind("<FocusIn>", self.clear_placeholder)
        self.domain_entry.bind("<Return>", lambda e: self.quick_recon())
        
        # Action buttons
        button_frame = ttk.Frame(input_frame, style="Main.TFrame")
        button_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, 
                  text="Quick Recon", 
                  command=self.quick_recon,
                  style="Primary.TButton").pack(side=tk.LEFT, padx=4)
        
        ttk.Button(button_frame, 
                  text="Clear", 
                  command=self.clear_domain,
                  style="Secondary.TButton").pack(side=tk.LEFT, padx=4)
        
        # Main content area
        content_frame = ttk.Frame(self.root, style="Main.TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        
        # Tabbed interface
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create organized tabs
        self.create_recon_tab(notebook)
        self.create_files_tab(notebook)
        self.create_tech_tab(notebook)
        self.create_vuln_tab(notebook)
        self.create_sensitive_tab(notebook)
        self.create_external_tab(notebook)
        self.create_cloud_tab(notebook)
        self.create_tools_tab(notebook)
        
        # Status console with scrollable text area
        console_frame = ttk.LabelFrame(self.root, text="Console Log", style="Card.TLabelframe", padding=8)
        console_frame.pack(fill=tk.X, padx=20, pady=8)
        
        # Create scrollable text widget for status
        self.console_text = tk.Text(console_frame, 
                                   height=4,  # Increased height for better visibility
                                   bg=self.card_bg, 
                                   fg=self.fg_color,
                                   font=("Consolas", 9),
                                   wrap=tk.WORD,
                                   relief="flat",
                                   borderwidth=1)
        
        # Scrollbar for console
        console_scrollbar = ttk.Scrollbar(console_frame, orient=tk.VERTICAL, command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=console_scrollbar.set)
        
        self.console_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        
        # Make console read-only
        self.console_text.config(state=tk.DISABLED)
        
        # Initial console message
        self.log_to_console("System initialized. Enter target domain to begin reconnaissance.")
        
        # Footer with full name
        footer_frame = ttk.Frame(self.root, style="Footer.TFrame")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=6)
        
        ttk.Label(footer_frame, 
                 text="Developed by Zishan Ahamed Thandar", 
                 font=("Segoe UI", 9),
                 style="Footer.TLabel").pack(side=tk.LEFT)
        
        # Links
        links_frame = ttk.Frame(footer_frame, style="Footer.TFrame")
        links_frame.pack(side=tk.RIGHT)
        
        portfolio_link = ttk.Label(links_frame, 
                                  text="Portfolio", 
                                  cursor="hand2", 
                                  font=("Segoe UI", 9),
                                  foreground=self.accent_color, 
                                  style="Footer.TLabel")
        portfolio_link.pack(side=tk.LEFT)
        portfolio_link.bind("<Button-1>", lambda e: webbrowser.open("https://ZishanAdThandar.github.io"))
        
        ttk.Label(links_frame, text=" • ", style="Footer.TLabel").pack(side=tk.LEFT)
        
        github_link = ttk.Label(links_frame, 
                               text="GitHub", 
                               cursor="hand2",
                               font=("Segoe UI", 9),
                               foreground=self.accent_color, 
                               style="Footer.TLabel")
        github_link.pack(side=tk.LEFT)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/ZishanAdThandar"))
    
    def clear_placeholder(self, event):
        """Clear placeholder text when entry is focused"""
        if self.domain_entry.get() == "example.com or https://example.com":
            self.domain_entry.delete(0, tk.END)
            self.domain_entry.config(fg=self.fg_color)
    
    def log_to_console(self, message):
        """Add message to console with timestamp"""
        self.console_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END)  # Auto-scroll to bottom
        self.console_text.config(state=tk.DISABLED)
    
    def setup_styles(self):
        """Configure tkinter styles for comfortable theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure main styles
        style.configure('Header.TFrame', background=self.bg_color)
        style.configure('Header.TLabel', background=self.bg_color, foreground=self.fg_color)
        style.configure('Main.TFrame', background=self.bg_color)
        style.configure('Custom.TLabel', background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        style.configure('Footer.TFrame', background=self.bg_color)
        style.configure('Footer.TLabel', background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 9))
        
        # Card and section styles
        style.configure('Card.TFrame', background=self.card_bg, relief='flat', borderwidth=0)
        style.configure('Card.TLabelframe', background=self.card_bg, foreground=self.fg_color)
        style.configure('Card.TLabelframe.Label', 
                       background=self.card_bg, 
                       foreground=self.accent_color, 
                       font=("Segoe UI", 10, "bold"))
        
        # Button styles
        style.configure('Primary.TButton', 
                       background=self.button_bg, 
                       foreground=self.fg_color,
                       borderwidth=0,
                       relief="flat",
                       font=("Segoe UI", 9),
                       padding=(12, 6))
        
        style.configure('Secondary.TButton', 
                       background=self.bg_color, 
                       foreground=self.highlight_color,
                       borderwidth=1,
                       relief="flat",
                       font=("Segoe UI", 9),
                       padding=(12, 6))
        
        # Notebook style
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=self.card_bg,
                       foreground=self.fg_color,
                       padding=[15, 6],
                       font=("Segoe UI", 9))
        
        # Button interactions
        style.map('Primary.TButton',
                 background=[('active', '#3a3a3a'), ('pressed', '#4a4a4a')],
                 foreground=[('active', self.highlight_color), ('pressed', self.highlight_color)])
        
        style.map('Secondary.TButton',
                 background=[('active', '#1a1a1a'), ('pressed', '#2a2a2a')],
                 foreground=[('active', self.accent_color), ('pressed', self.accent_color)])
        
        style.map('TNotebook.Tab',
                 background=[('selected', '#2a2a2a'), ('active', '#3a3a3a')],
                 foreground=[('selected', self.accent_color), ('active', self.highlight_color)])

    def create_section(self, parent, title, buttons, columns=2):
        """Create a section with title and buttons in grid layout"""
        section_frame = ttk.LabelFrame(parent, text=title, style="Card.TLabelframe", padding=10)
        section_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)
        
        for i, (text, command, tooltip) in enumerate(buttons):
            row = i // columns
            col = (i % columns) * 2
            btn = ttk.Button(section_frame, 
                           text=text, 
                           command=command, 
                           width=26, 
                           style="Primary.TButton")
            btn.grid(row=row, column=col, padx=6, pady=4, sticky=tk.W)
            if tooltip:
                self.create_tooltip(btn, tooltip)

    def create_tooltip(self, widget, text):
        """Create comfortable tooltips"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+15}+{event.y_root+15}")
            tooltip.configure(background=self.card_bg, relief='solid', borderwidth=1)
            label = ttk.Label(tooltip, 
                            text=text, 
                            background=self.card_bg, 
                            foreground=self.fg_color,
                            font=("Segoe UI", 9),
                            relief='solid', 
                            borderwidth=1, 
                            padding=8)
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
            ("🌐 Subdomains Discovery", self.subdomains_search, "Find subdomains (*.domain.com)"),
            ("📜 SSL Certificates", self.certificate_search, "Search SSL certificates on crt.sh"),
            ("🕵️ Wayback Machine", self.wayback_machine, "Check historical site data"),
            ("🌐 DNS Information", self.dns_recon, "DNS information and records"),
            ("🔄 Reverse IP Lookup", self.reverse_ip, "Find other sites on same IP"),
            ("🛡️ Security Headers", self.security_headers, "Analyze security headers"),
            ("📊 WHOIS Information", self.whois_lookup, "Domain registration details"),
            ("🔍 Port Scan", self.port_scan, "Check open ports via Shodan"),
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
            ("🔐 SSH Keys", self.ssh_keys, "Find SSH private keys"),
            ("🔑 SSL Cert Files", self.ssl_certs, "Find SSL certificate files"),
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
            ("☕ Java Files", self.java_files, "Find JSP, Java configuration files"),
            ("🔗 WSDL Files", self.wsdl_files, "Find web service definition files"),
            ("📊 CMS Detection", self.cms_detection, "Detect CMS and technologies"),
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
            ("⚡ Web Shells", self.shells_backdoors, "Find web shells and backdoors"),
            ("🌐 Crossdomain Policy", self.crossdomain_xml, "Check crossdomain.xml policies"),
            ("🤖 Robots.txt", self.robots_txt, "Check robots.txt for sensitive paths"),
            ("💉 XSS Parameters", self.xss_points, "Find potential XSS vulnerable parameters"),
            ("📧 Email Harvesting", self.email_harvest, "Find email addresses"),
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
            ("🏦 Financial Information", self.financial_data, "Find financial data"),
            ("📊 Analytics Data", self.analytics_data, "Find analytics and tracking data"),
            ("🔐 Password Files", self.password_files, "Find password files"),
            ("📝 Config Secrets", self.config_secrets, "Find secrets in config files"),
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
            ("📹 YouTube Content", self.youtube_search, "Search YouTube for related content"),
            ("👨‍💼 Stack Overflow", self.stack_overflow, "Search Stack Overflow for code"),
            ("🐱 GitLab Repos", self.gitlab_search, "Search GitLab for exposed repos"),
            ("📚 Confluence Pages", self.confluence_search, "Search Confluence pages"),
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
            ("📡 Censys Search", self.censys_search, "Search Censys for infrastructure"),
            ("🍃 Google Cloud Storage", self.google_cloud, "Find Google Cloud Storage"),
            ("🔥 Firebase Databases", self.firebase_search, "Find Firebase databases"),
            ("☁️ Heroku Apps", self.heroku_search, "Find Heroku applications"),
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
            ("🔧 URL Fuzzing", self.url_fuzzer, "Common path and file fuzzing"),
            ("📄 Sitemap Search", self.sitemap_generator, "Generate sitemap.xml"),
            ("🔗 Reverse Image Search", self.reverse_image_search, "Search by image"),
            ("📝 Data Leak Check", self.leak_check, "Check for data leaks"),
        ]
        self.create_section(tools_frame, "Custom Tools", buttons, columns=2)

    # === Utility Methods ===
    def get_domain(self):
        input_text = self.domain_entry.get().strip()
        if not input_text or input_text == "example.com or https://example.com":
            messagebox.showwarning("Input Required", "Please enter a target domain")
            return None
        
        # Extract domain from URL if needed
        domain = self.extract_domain(input_text)
        if not domain:
            messagebox.showwarning("Invalid Input", "Please enter a valid domain")
            return None
            
        return domain

    def open_url(self, url):
        try:
            webbrowser.open(url)
            self.log_to_console(f"Search opened: {url}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open URL: {str(e)}")

    # === RECONNAISSANCE METHODS ===
    def subdomains_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:*.{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"Subdomain discovery for {domain}")

    def certificate_search(self):
        if domain := self.get_domain():
            url = f"https://crt.sh/?q={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"SSL certificate search for {domain}")

    def wayback_machine(self):
        if domain := self.get_domain():
            url = f"https://web.archive.org/web/*/{urllib.parse.quote(domain)}/*"
            self.open_url(url)
            self.log_to_console(f"Wayback Machine search for {domain}")

    def dns_recon(self):
        if domain := self.get_domain():
            url = f"https://viewdns.info/dnsrecord/?domain={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"DNS reconnaissance for {domain}")

    def reverse_ip(self):
        if domain := self.get_domain():
            url = f"https://viewdns.info/reverseip/?host={urllib.parse.quote(domain)}&t=1"
            self.open_url(url)
            self.log_to_console(f"Reverse IP lookup for {domain}")

    def security_headers(self):
        if domain := self.get_domain():
            url = f"https://securityheaders.com/?q={urllib.parse.quote(domain)}&followRedirects=on"
            self.open_url(url)
            self.log_to_console(f"Security headers check for {domain}")

    def whois_lookup(self):
        if domain := self.get_domain():
            url = f"https://whois.domaintools.com/{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"WHOIS lookup for {domain}")

    def port_scan(self):
        if domain := self.get_domain():
            url = f"https://www.shodan.io/host/{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"Port scan for {domain}")

    # === FILE DISCOVERY METHODS ===
    def open_directories(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intitle:index.of"
            self.open_url(url)
            self.log_to_console(f"Open directories search for {domain}")

    def config_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:xml+|+ext:conf+|+ext:cnf+|+ext:reg+|+ext:inf+|+ext:rdp+|+ext:cfg+|+ext:txt+|+ext:ora+|+ext:ini+|+ext:env"
            self.open_url(url)
            self.log_to_console(f"Configuration files search for {domain}")

    def database_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:sql+|+ext:dbf+|+ext:mdb+|+ext:db+|+ext:sqlite+|+ext:dump"
            self.open_url(url)
            self.log_to_console(f"Database files search for {domain}")

    def log_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:log+|+ext:logs"
            self.open_url(url)
            self.log_to_console(f"Log files search for {domain}")

    def backup_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:bkf+|+ext:bkp+|+ext:bak+|+ext:old+|+ext:backup+|+ext:tar.gz+|+ext:tgz+|+ext:zip"
            self.open_url(url)
            self.log_to_console(f"Backup files search for {domain}")

    def documents(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:doc+|+ext:docx+|+ext:odt+|+ext:pdf+|+ext:rtf+|+ext:sxw+|+ext:psw+|+ext:ppt+|+ext:pptx+|+ext:pps+|+ext:csv+|+ext:xls+|+ext:xlsx"
            self.open_url(url)
            self.log_to_console(f"Documents search for {domain}")

    def ssh_keys(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:key+|+ext:pem+|+ext:ppk+|+ext:pub+%22ssh%22"
            self.open_url(url)
            self.log_to_console(f"SSH keys search for {domain}")

    def ssl_certs(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:crt+|+ext:pem+|+ext:cer+|+ext:der"
            self.open_url(url)
            self.log_to_console(f"SSL certificates search for {domain}")

    # === TECHNOLOGY DETECTION METHODS ===
    def wordpress(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:wp-+|+inurl:wp-content+|+inurl:plugins+|+inurl:uploads+|+inurl:themes"
            self.open_url(url)
            self.log_to_console(f"WordPress reconnaissance for {domain}")

    def php_info(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:php+intitle:phpinfo+%22published+by+the+PHP+Group%22"
            self.open_url(url)
            self.log_to_console(f"PHP info pages search for {domain}")

    def apache_config(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+filetype:config+%22apache%22"
            self.open_url(url)
            self.log_to_console(f"Apache config files search for {domain}")

    def env_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:env+|+inurl:.env+%22API%22+%22KEY%22"
            self.open_url(url)
            self.log_to_console(f"Environment files search for {domain}")

    def django_debug(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intext:%22DEBUG+%3D+True%22+|+intext:%22settings.DEBUG%22"
            self.open_url(url)
            self.log_to_console(f"Django debug mode search for {domain}")

    def java_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:jsp+|+ext:jspx+|+ext:java+|+ext:class+|+ext:war"
            self.open_url(url)
            self.log_to_console(f"Java files search for {domain}")

    def wsdl_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+filetype:wsdl+|+filetype:WSDL+|+ext:svc+|+inurl:wsdl"
            self.open_url(url)
            self.log_to_console(f"WSDL files search for {domain}")

    def cms_detection(self):
        if domain := self.get_domain():
            url = f"https://whatcms.org/?s={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"CMS detection for {domain}")

    # === VULNERABILITY SCANNING METHODS ===
    def sql_errors(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intext:%22sql+syntax+near%22+|+intext:%22syntax+error+has+occurred%22+|+intext:%22Warning:+mysql_connect()%22"
            self.open_url(url)
            self.log_to_console(f"SQL errors search for {domain}")

    def login_pages(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:login+|+inurl:signin+|+intitle:Login+|+intitle:signin+|+inurl:auth"
            self.open_url(url)
            self.log_to_console(f"Login pages search for {domain}")

    def redirects(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:redir+|+inurl:url+|+inurl:redirect+|+inurl:return+|+inurl:src=http"
            self.open_url(url)
            self.log_to_console(f"Open redirects search for {domain}")

    def shells_backdoors(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:shell+|+inurl:backdoor+|+inurl:wso+|+inurl:c99+|+inurl:r57"
            self.open_url(url)
            self.log_to_console(f"Web shells search for {domain}")

    def crossdomain_xml(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q={urllib.parse.quote(domain)}/crossdomain.xml"
            self.open_url(url)
            self.log_to_console(f"Crossdomain policy check for {domain}")

    def robots_txt(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q={urllib.parse.quote(domain)}/robots.txt"
            self.open_url(url)
            self.log_to_console(f"Robots.txt check for {domain}")

    def xss_points(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:?+|+inurl:&+|+inurl:query+|+inurl:search+|+inurl:redirect"
            self.open_url(url)
            self.log_to_console(f"XSS vulnerable points search for {domain}")

    def email_harvest(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22@%22+%22email%22+%22contact%22"
            self.open_url(url)
            self.log_to_console(f"Email harvesting for {domain}")

    # === SENSITIVE DATA METHODS ===
    def api_keys(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22api_key%22+|+%22api+key%22+|+%22secret_key%22+|+%22password%22+filetype:env"
            self.open_url(url)
            self.log_to_console(f"API keys search for {domain}")

    def email_lists(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:csv+|+ext:xls+|+ext:xlsx+%22email%22+%22password%22"
            self.open_url(url)
            self.log_to_console(f"Email lists search for {domain}")

    def exposed_users(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+intitle:%22index+of%22+%22users%22+|+inurl:%22user+profiles%22"
            self.open_url(url)
            self.log_to_console(f"Exposed users search for {domain}")

    def payment_info(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22payment%22+|+%22credit+card%22+|+%22paypal%22+filetype:csv"
            self.open_url(url)
            self.log_to_console(f"Payment information search for {domain}")

    def financial_data(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22financial%22+|+%22bank%22+|+%22account%22+filetype:xls"
            self.open_url(url)
            self.log_to_console(f"Financial data search for {domain}")

    def analytics_data(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22analytics%22+|+%22tracking%22+|+%22google+analytics%22"
            self.open_url(url)
            self.log_to_console(f"Analytics data search for {domain}")

    def password_files(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22password%22+filetype:txt+|+filetype:log"
            self.open_url(url)
            self.log_to_console(f"Password files search for {domain}")

    def config_secrets(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+%22secret%22+|+%22token%22+|+%22key%22+filetype:env"
            self.open_url(url)
            self.log_to_console(f"Config secrets search for {domain}")

    # === EXTERNAL RECON METHODS ===
    def github_search(self):
        if domain := self.get_domain():
            url = f"https://github.com/search?q=%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"GitHub search for {domain}")

    def pastebin_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:pastebin.com+{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"Pastebin search for {domain}")

    def linkedin_employees(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:linkedin.com+employees+{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"LinkedIn employees search for {domain}")

    def reddit_search(self):
        if domain := self.get_domain():
            url = f"https://www.reddit.com/search/?q={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"Reddit search for {domain}")

    def youtube_search(self):
        if domain := self.get_domain():
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"YouTube search for {domain}")

    def stack_overflow(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:stackoverflow.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"Stack Overflow search for {domain}")

    def gitlab_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=inurl:gitlab+{urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"GitLab search for {domain}")

    def confluence_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:*.atlassian.net+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"Confluence search for {domain}")

    # === CLOUD INFRASTRUCTURE METHODS ===
    def s3_buckets(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:.s3.amazonaws.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"S3 buckets search for {domain}")

    def digitalocean_spaces(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:digitaloceanspaces.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"DigitalOcean Spaces search for {domain}")

    def azure_blobs(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:blob.core.windows.net+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"Azure Blobs search for {domain}")

    def shodan_search(self):
        if domain := self.get_domain():
            url = f"https://www.shodan.io/search?query={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"Shodan search for {domain}")

    def censys_search(self):
        if domain := self.get_domain():
            url = f"https://censys.io/ipv4?q={urllib.parse.quote(domain)}"
            self.open_url(url)
            self.log_to_console(f"Censys search for {domain}")

    def google_cloud(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:storage.googleapis.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"Google Cloud Storage search for {domain}")

    def firebase_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:firebaseio.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"Firebase search for {domain}")

    def heroku_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:herokuapp.com+%22{urllib.parse.quote(domain)}%22"
            self.open_url(url)
            self.log_to_console(f"Heroku search for {domain}")

    # === CUSTOM TOOLS METHODS ===
    def custom_dork_search(self):
        if domain := self.get_domain():
            dork = simpledialog.askstring("Custom Dork", "Enter your Google dork:")
            if dork:
                url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+{urllib.parse.quote(dork)}"
                self.open_url(url)
                self.log_to_console(f"Custom dork search for {domain}: {dork}")

    def quick_scan(self):
        if domain := self.get_domain():
            self.log_to_console(f"Starting quick reconnaissance scan for {domain}")
            # Run multiple common searches
            searches = [
                self.subdomains_search,
                self.open_directories,
                self.config_files,
                self.login_pages,
                self.backup_files,
                self.php_info
            ]
            for search in searches:
                search()
            self.log_to_console("Quick scan completed - multiple searches opened")

    def url_fuzzer(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+inurl:admin+|+inurl:login+|+inurl:test+|+inurl:backup"
            self.open_url(url)
            self.log_to_console(f"URL fuzzing for {domain}")

    def sitemap_generator(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+filetype:xml+%22sitemap%22"
            self.open_url(url)
            self.log_to_console(f"Sitemap search for {domain}")

    def reverse_image_search(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=site:{urllib.parse.quote(domain)}+ext:jpg+|+ext:png+|+ext:gif"
            self.open_url(url)
            self.log_to_console(f"Reverse image search for {domain}")

    def leak_check(self):
        if domain := self.get_domain():
            url = f"https://www.google.com/search?q=%22{urllib.parse.quote(domain)}%22+%22password%22+%22leak%22+%22breach%22"
            self.open_url(url)
            self.log_to_console(f"Leak check for {domain}")

    def quick_recon(self):
        if domain := self.get_domain():
            self.quick_scan()

    def clear_domain(self):
        self.domain_entry.delete(0, tk.END)
        self.domain_entry.insert(0, "example.com or https://example.com")
        self.domain_entry.config(fg="gray")
        self.log_to_console("Domain field cleared")

    def run(self):
        """Start the application main loop"""
        self.root.mainloop()

def main():
    """Main entry point for the GUI application"""
    app = WebsiteDorkerPro()
    app.run()

if __name__ == "__main__":
    main()
