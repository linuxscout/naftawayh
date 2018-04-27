#!/usr/bin/python
from setuptools import setup

# to install type:
# python setup.py install --root=/

setup(name='Naftawayh', version='0.3',
      description='Naftawayh: Arabic word tagger',
      author='Taha Zerrouki',
      author_email='taha.zerrouki@gmail.com',
      url='http://naftawayh.sourceforge.net/',
      license='GPL',
      package_dir={'naftawayh': 'naftawayh'},
      packages=['naftawayh'],
      install_requires=[ 'pyarabic','tashaphyne',
      ],   
      include_package_data=True,

      package_data = {
        'naftawayh': ['doc/*.*','doc/html/*'],
        },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: End Users/Desktop',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
    );

