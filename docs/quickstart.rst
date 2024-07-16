Quick-Start Guide
=================

This quick-start guide will help you get up and running with `pocketpartition` quickly.

Installation
------------

To install `pocketpartition`, use pip:

.. code-block:: bash

    pip install git+https://github.com/blackgauss/pocketpartition.git

To update Pocket Partition run the following command:

.. code-block:: bash

    pip install --upgrade git+https://github.com/blackgauss/pocketpartition.git

Basic Usage
-----------

Here's a simple example to get you started:

.. code-block:: python

    import pocketpartition import NumericalSet, NumericalSemigroup, atom_monoid

    # Make a Numerical Set
    T = NumericalSet(gaps=[1,2,3,9,11,15])
    
    # Get its Atom Monoid
    S = atom_monoid(T)

    # Minimal Generating Set
    print(S.minimal_generating_set())

More Information
----------------

For more detailed information, refer to the full documentation available at :ref:`genindex`.

