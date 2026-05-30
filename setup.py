#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="samsung-a12-unlocker",
    version="2.0.0",
    author="Your Name",
    description="Samsung Galaxy A12 Unlock Tool",
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
        'beautifulsoup4>=4.11.0',
        'colorama>=0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'a12-unlocker=src.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.8',
)
