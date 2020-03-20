from setuptools import setup
from setuptools import find_packages
from temlogger import __version__


with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='temlogger',
    version=__version__,
    description='Python logging handler for Logstash and StackDriver.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/tembici/temlogger',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ],
    install_requires=[
        'google-cloud-logging>=1.14.0,<2',
        'python3-logstash==0.4.80'
    ]
)
