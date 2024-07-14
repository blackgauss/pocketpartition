from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pocketpartition',
    version='0.2.0',
    package_dir={"":"src"},
    packages=find_packages(where="src"),  # No need to specify 'where' if everything is at the top level
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
