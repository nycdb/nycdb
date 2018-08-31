import setuptools

setuptools.setup(
    name="nycdb",
    version="0.1.8",
    url="https://github.com/aepyornis/nyc-db",

    author="ziggy",
    author_email="nycdb@riseup.net",

    license='AGPL-3.0-or-later',

    description="database of nyc housing data",
    long_description=open('README.rst').read(),

    entry_points={
        'console_scripts': [
            'nycdb=nycdb.cli:main'
        ],
    },

    packages=['nycdb'],

    package_data={
        'nycdb': [
            'datasets.yml',
            'sql/*.sql',
            'sql/**/*.sql'
        ]
    },

    include_package_data=True,

    python_requires='>=3',

    install_requires=[
        'PyYAML>=3',
        'requests>=2.18',
        'xlrd>=1.1.0',
        'pyproj>=1.9.5',
        'psycopg2>=2.7'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
