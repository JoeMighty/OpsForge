from setuptools import setup, find_packages

setup(
    name="opsforge",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "rich",
        "pyyaml",
        "requests",
        "boto3",
        "scapy",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "opsforge=opsforge.main:cli",
        ],
    },
    author="JoeMighty",
    author_email="18178462+JoeMighty@users.noreply.github.com",
    description="Consolidated toolkit for cybersecurity and cloud infrastructure.",
    url="https://github.com/JoeMighty/OpsForge",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
