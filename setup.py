from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.md')).read()
except:
    README = 'ESXi Management Utility'

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    "Programming Language :: Python :: 3.8.5",
]

setup(
    name='slackreplybot',
    version='1.0.0.0',
    description='A Slack Reply Bot',
    classifiers=CLASSIFIERS,
    author='Ryan Chapin',
    author_email='rchapin@nbinteractive.com',
    long_description=README,
    url='',
    python_requires='>=3.8.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
         'console_scripts': [
             'slackreplybot=slackreplybot.main:main',
             ],
    },
)
