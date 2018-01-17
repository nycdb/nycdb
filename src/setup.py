import setuptools

setuptools.setup(
    name="nycdb",
    version="0.1.0",
    url="https://github.com/aepyornis/nyc-db",

    author="ziggy",
    author_email="nycdb@riseup.net",

    license='GPL',

    description="database of nyc housing data",
    long_description=open('README.md').read(),

    packages=['nycdb'],

    python_requires='>=3',

    install_requires=[
        'Cython>=0.27',
        'PyYAML>=3',
        'requests>=2.18',
        'xlrd>=1.1.0',
        'pyproj>=1.9.5',
        'psycopg2>=2.7'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
