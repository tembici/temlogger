from distutils.core import setup

__version__ = '0.2.3'


setup(
    name='temlogger',
    packages=['temlogger'],
    version=__version__,
    description='Python logging handler for Logstash and StackDriver.',
    long_description=open('README.md').read(),
    url='https://github.com/tembici/temlogger',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6+',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ],
    install_requires=[
        'google-cloud-logging>=1.14.0,<2',
        'python3-logstash==0.4.80'
    ]
)
