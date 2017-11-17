import setuptools

setuptools.setup(
    name="nycdb",
    version="0.1.0",
    url="https://github.com/aepyornis/nyc-db",

    author="ziggy",
    author_email="ziggy@elephant-bird.net",

    description="nyc housing database",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(exclude=('tests', 'docs')),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
