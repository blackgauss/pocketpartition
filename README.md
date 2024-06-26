
# Pocket -| Partition

This package provides two main classes: `NumericalSet` and `Partition`. These classes are designed to handle operations related to numerical sets and partitions, commonly used in combinatorics and number theory.

## Installation

To install the package, simply clone the repository and install it using pip:

```bash
git clone https://github.com/yourusername/numericalset-partition.git
cd numericalset-partition
pip install .
```

## Usage

### NumericalSet Class

The `NumericalSet` class is used to handle numerical sets and perform operations such as computing the atom monoid and the Apéry set.

#### Initialization

```python
from numericalset import NumericalSet

gaps = [1, 2, 4]
numerical_set = NumericalSet(gaps)
```

#### Methods

- `atom_monoid()`: Computes the gaps of the atom monoid.

    ```python
    gaps_atom_monoid = numerical_set.atom_monoid()
    ```

- `apery_set(n)`: Computes the Apéry set of the numerical set with respect to `n`.

    ```python
    apery_set = numerical_set.apery_set(3)
    ```

### Partition Class

The `Partition` class is used to handle partitions and perform operations such as computing the conjugate partition, hook lengths, profile, and gaps.

#### Initialization

```python
from partition import Partition

partition = [4, 3, 1]
partition_obj = Partition(partition)
```

#### Methods

- `conjugate()`: Computes the conjugate partition.

    ```python
    conjugate_partition = partition_obj.conjugate()
    ```

- `hook_lengths(i=None, j=None)`: Computes the hook length of a cell in the partition. If `i` and `j` are not provided, computes the hook lengths for all cells.

    ```python
    hook_lengths = partition_obj.hook_lengths()
    single_hook_length = partition_obj.hook_lengths(i=1, j=2)
    ```

- `profile()`: Computes the profile of the partition as a series of moves ("Right" and "Up").

    ```python
    profile = partition_obj.profile()
    ```

- `gaps()`: Computes the gaps in the profile of the partition.

    ```python
    gaps = partition_obj.gaps()
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
