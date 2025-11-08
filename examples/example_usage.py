#!/usr/bin/env python3
"""
Example usage of WebsiteDorkerPro
"""

from website_dorker_pro import WebsiteDorkerPro
import tkinter as tk

def example_gui():
    """Example of using the GUI"""
    root = tk.Tk()
    app = WebsiteDorkerPro(root)
    app.run()

def example_cli_equivalent():
    """Example of CLI equivalent functionality"""
    from website_dorker_pro.cli import WebsiteDorkerProCLI
    
    cli = WebsiteDorkerProCLI()
    
    # Quick scan
    cli.quick_scan("example.com")
    
    # Specific search
    cli.search("example.com", "subdomains")

if __name__ == "__main__":
    print("WebsiteDorkerPro Examples")
    print("1. Run GUI: example_gui()")
    print("2. Run CLI equivalent: example_cli_equivalent()")
