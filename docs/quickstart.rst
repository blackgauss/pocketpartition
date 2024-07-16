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
    print(P.display(show_hooks=True))

    # Get help on all methods of a certain class
    help(S)

More Information
----------------

For more detailed information, refer to the full documentation available at :ref:`genindex`.

