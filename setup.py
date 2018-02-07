from setuptools import setup, find_packages

requires=['rauth', 'six']

setup(name='contextio',
    version='v1.12.8',
    description='Library for accessing the Context.IO API (v2.0 and Lite) in Python',
    author='Alex Tanton, Cecy Correa',
    author_email='alex.tanton@returnpath.com, cecy.correa@returnpath.com',
    url='http://context.io',
    keywords=['contextIO', 'imap', 'oauth'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    download_url='https://github.com/contextio/Python-ContextIO/archive/v1.12.8.tar.gz',
)
