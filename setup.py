from setuptools import setup


require_libs = ['plyvel>=1.0.5']


with open('README.md') as f:
    long_description = f.read().strip()


setup(
    name='diff_trigger',
    description='decorator for monitor function result, run callback when result has been changed',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    version='1.0.0',
    author='thuhak',
    author_email='thuhak.zhou@nio.com',
    keywords='decorator',
    packages =['diff_trigger'],
    url='https://github.com/thuhak/diff_trigger',
    install_requires=require_libs
)
