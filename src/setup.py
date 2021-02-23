import setuptools

setuptools.setup(
    name="nycdb",
    version="0.2.0",
    url="https://github.com/nycdb/nycdb",
    author="nycdb",
    author_email="nycdb@riseup.net",
    license='AGPL-3.0-or-later',
    description="database of nyc housing data",
    long_description=open('README.md').read(),
    long_description_content_type=('text/markdown'),

    entry_points={
        'console_scripts': [
            'nycdb=nycdb.cli:main'
        ],
    },

    packages=['nycdb'],

    package_data={
        'nycdb': [
            'datasets/*.yml',
            'sql/*.sql',
            'sql/**/*.sql'
        ]
    },

    include_package_data=True,

    python_requires='>=3',

    install_requires=[
        'PyYAML>=5.1',
        'requests>=2.18',
        'xlrd>=1.1.0',
        'pyproj>=2.1.3',
        'psycopg2>=2.7',
        'tqdm>=4.28.1'
    ],

    extras_requires={
        'test': ['pytest>=6']
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
