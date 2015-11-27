from distutils.core import setup, Extension

module1 = Extension('exmod', 
					include_dirs = ['/usr/local/include'],
				    libraries = ['pthread'],
					sources =['find_route.cpp'])

setup (name = 'exmod',
	   version ='1.0',
	   description = 'This is for find route',
	   author ='Mark',
	   ext_modules = [module1])