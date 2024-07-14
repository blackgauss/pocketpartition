# Pocket -| Partition
# Pocket Partition Documentation

Pocket Partition is a Python package designed for handling numerical sets and partitions. It provides classes and methods for operations related to mathematical partitions, including computing gaps, non-gaps, and working with numerical semigroups.

## Repository Structure

The repository is structured as follows:

- `pocketpartition/`: Main package directory.
  - `example_usage.ipynb`: Jupyter notebook with examples of how to use the package.
  - `numerical.py`: Module containing classes for numerical sets and semigroups.
  - `partition.py`: Module providing the `Partition` class for partition operations.
- `README.md`: The main documentation file for the repository.
- `setup.py`: Script for installing the package.
- `tests/`: Directory containing unit tests.
  - `__pycache__/`: Compiled Python files for tests.
  - `test_numerical_partition.py`: Unit tests for numerical set and partition functionalities.

## Main Components

### Numerical Module

The `numerical.py` module includes classes for working with numerical sets and semigroups:

- `NumericalSet`: Base class for numerical sets.
- `NumericalSemigroup`: Inherits from `NumericalSet`, specialized for semigroup operations.

### Partition Module

The `partition.py` module provides the `Partition` class, which supports various operations on mathematical partitions, such as computing gaps and non-gaps within a numerical set.

### Example Usage

The `example_usage.ipynb` Jupyter notebook demonstrates how to use the package's functionalities, including creating partitions, computing hook lengths, and checking if a partition forms a semigroup.

## Installation

To install Pocket Partition, run the following command:


```sh
pip install git+https://github.com/blackgauss/pocketpartition.git
```

To update Pocket Partition run the following command:

```sh
pip install --upgrade git+https://github.com/blackgauss/pocketpartition.git
```

# Numerical Module Documentation

The `numerical.py` module in the Pocket Partition package provides classes and functions for working with numerical sets and semigroups. It is designed to facilitate operations such as partitioning numerical sets, computing small elements, and handling numerical semigroups.

## Classes

### NumericalSet

The `NumericalSet` class represents a set of numbers and provides methods for various operations on these sets.

### NumericalSemigroup

The `NumericalSemigroup` class is a subclass of `NumericalSet` and represents a numerical semigroup, which is a special kind of numerical set with additional properties and operations.

Inherits all methods from `NumericalSet`.

# Partition Module Documentation

The `partition.py` module in the Pocket Partition package provides a `Partition` class designed for handling mathematical partitions, including operations like computing gaps and non-gaps within a numerical set.

## Classes

### Partition

The `Partition` class represents a mathematical partition and provides methods for operations related to numerical partitions.

#### Methods

## Usage Example

See `example_usage.ipynb` notebook