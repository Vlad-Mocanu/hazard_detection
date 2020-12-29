# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hazard_detector',
    version='1.0.0',
    description='Notifies via e-mail the presence of water (flood) and motor (pump) not stopping malfunction',
    long_description=long_description,
    url='https://github.com/Vlad-Mocanu/hazard_detection',
    author='Vlad Mocanu',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache 2.0 License',
        'Programming Language :: Python :: 3.7.3',
    ],
    keywords='microphone humidity water sound sensors email',
        install_requires=[
                'pyaudio>=0.2.11',
                'numpy>=1.16.2'
        ]
)
