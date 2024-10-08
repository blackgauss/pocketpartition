from setuptools import setup, find_packages

setup(
    name='pocketpartition',
    version='1.1.3-alpha',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/blackgauss/pocketpartition',
    license='MIT',
    author='Erik Imathiu-Jones',
    author_email='eimathiucaltech@gmail.com',
    description='A package for handling numerical sets, semigroups and partitions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    test_suite='tests',
)