# Pocket -| Partition
# Pocket Partition Documentation

Pocket Partition is a Python package designed for handling numerical sets and partitions.

For more detailed information, refer to the full documentation available at [Read the Docs](https://pocketpartition.readthedocs.io/en/latest/).

## Installation

To install Pocket Partition, run the following command:


```sh
pip install git+https://github.com/blackgauss/pocketpartition.git
```

To update Pocket Partition run the following command:

```sh
pip install --upgrade git+https://github.com/blackgauss/pocketpartition.git
```

## Basic Usage

Here's a simple example to get you started:

```python
from pocketpartition import NumericalSet, NumericalSemigroup, get_atom_monoid, get_partition

# Make a numerical set
T = NumericalSet(gaps=[1,2,3,9,11,15])

# Get its atom monoid
S = get_atom_monoid(T)

# Minimal Generating Set
print(S.minimal_generating_set())

# Get its partition
P = get_partition(T)

# Display Partition with hooks
P.display(show_hooks=True)

# Get help on all methods of a certain class
help(S)
```

## WARNING

This package can work alongside SageMath and the `numericalsgps` package. However, there are a few important points to note:

1. **Namespace Conflicts**: To avoid conflicts with the `numericalsgps` package, import `pocketpartition` using an alias, such as `pp` or another name.
   ```python
   import pocketpartition as pp
   ```

2. **Type Conversion**: SageMath uses its own `Integer()` type, which is different from Python's `int()`. You may need to convert `Integer()` types to `int()` before using them with `pocketpartition`.
   ```python
   n = int(Integer(5))  # Convert SageMath Integer to Python int
   ```

### Frequently Asked Questions

**Q: I already have SageMath and the `numericalsgps` package. Why do I need this?**

**A:** This package is particularly useful for working with the correspondences between numerical sets, partitions, numerical semigroups, and posets.

## Theory References
W.I.P.

## Code References

Some functions/classes inspired by 
- Sagemath [SageMath GitHub repository](https://github.com/sagemath/sage).
- Numerical Semigroups package for GAP [numericalsgps GitHub repository](https://github.com/gap-packages/numericalsgps)

