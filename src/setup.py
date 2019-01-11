import os
import setuptools

MY_DIR = os.path.abspath(os.path.dirname(__file__))

TEST_DATA_RELATIVE_DIR = os.path.join('tests', 'integration', 'data')

TEST_DATA_DIR = os.path.join(MY_DIR, TEST_DATA_RELATIVE_DIR)

TEST_DATA_FILES = [
    os.path.join(TEST_DATA_RELATIVE_DIR, filename)
    for filename in os.listdir(TEST_DATA_DIR)
]

setuptools.setup(
    name="nycdb",
    version="0.1.15",
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

    data_files=[
        ('nycdb_test_data', TEST_DATA_FILES),
    ],

    include_package_data=True,

    python_requires='>=3',

    install_requires=[
        'PyYAML>=3',
        'requests>=2.18',
        'xlrd>=1.1.0',
        'pyproj>=1.9.5',
        'psycopg2>=2.7',
        'tqdm>=4.28.1'
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
