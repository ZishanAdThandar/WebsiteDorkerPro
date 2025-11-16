from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="website-dorker-pro",
    version="1.1.0",  # ← Updated version
    author="Zishan Ahamed Thandar",  # ← Updated full name
    author_email="your-email@example.com",  # Update with your actual email
    description="Website Reconnaissance Toolkit for Bug Hunters and Pentesters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZishanAdThandar/WebsiteDorkerPro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],  # tkinter is usually included
    entry_points={
        "console_scripts": [
            "websitedorkerpro=website_dorker_pro.cli:main",
            "wdp=website_dorker_pro.cli:main",
        ],
    },
    keywords=[
        "bug-bounty",
        "reconnaissance", 
        "penetration-testing",
        "security",
        "dorking",
        "osint"
    ],
)
