#          Copyright Rein Halbersma 2020-2021.
# Distributed under the Boost Software License, Version 1.0.
#    (See accompanying file LICENSE_1_0.txt or copy at
#          http://www.boost.org/LICENSE_1_0.txt)

from setuptools import setup, find_packages

setup(
    name='scrape',
    version='0.1.0-dev0',
    description='Exercises in web scraping',
    url='https://github.com/rhalbersma/scrape',
    author='Rein Halbersma',
    author_email='rhalbersma@gmail.com',
    license='Boost Software License 1.0 (BSL-1.0)',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'bs4', 'lxml', 'notebook', 'numpy', 'pandas', 'plotnine', 'pylint', 'requests', 'tqdm', 'xlrd'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 7 - Inactive'
        'Intended Audience :: Science/Research'
        'License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
