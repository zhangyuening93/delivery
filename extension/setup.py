from distutils.core import setup, Extension

module1 = Extension('spam',
					include_dirs = ['/usr/local/include'],
					library_dirs = ['/usr/local/lib'],
                    sources = ['spammify.c'])

setup (name = 'spam',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])