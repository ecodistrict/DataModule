from setuptools import setup

setup(name='DataModule',
      version='0.1.0',
      packages=['DataModule'],
      entry_points={
          'console_scripts': [
              'DataModule = DataModule.__main__:main'
          ]
      },
      )