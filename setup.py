from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='Zeek-Indenter',
	version='0.1.0',
	description='Python package to indent Zeek scripts.',
	long_description=long_description,
	url='http://pypi.python.org/pypi/ZeekIndenter/',
	author='Mohan Dhawan',
	author_email='mohan@corelight.com',
	packages=find_packages(),
	python_requires='>=3.6',
	install_requires=['lark-parser'],
	package_data={
		'indenter': ['*.txt', 'utils/zeek.lark', 'utils/zeek-lalr.lark', 'utils/zeek-earley.lark']
	},
	classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)