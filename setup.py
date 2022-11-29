from distutils.core import setup # Need this to handle modules
import py2exe 
import math # We have to import all modules used in our program

setup(windows=['M2_config_manual_parameters.py']) # Calls setup function to indicate that we're dealing with a single console application