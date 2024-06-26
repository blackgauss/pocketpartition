import unittest
import random
from pocketpartition.pocketpartition import Partition, NumericalSet

def generate_random_partition():
    length = random.randint(1, 10)  # Random length of the partition
    partition = sorted([random.randint(1, 20) for _ in range(length)], reverse=True)
    return partition

class TestNumericalSetPartition(unittest.TestCase):

    def test_partition_and_numerical_set(self):
        for _ in range(100):  # Number of random tests
            partition_list = generate_random_partition()

            # Create Partition object
            l = Partition(partition_list)

            # Get gaps from Partition
            partition_gaps = l.gaps()

            # Create NumericalSet object using gaps
            T = NumericalSet(partition_gaps)

            # Get partition from NumericalSet
            numerical_set_partition = T.partition()

            # Assert that the partitions are equal
            self.assertEqual(numerical_set_partition, partition_list, 
                             f"Test failed: {numerical_set_partition} != {partition_list}")

if __name__ == "__main__":
    unittest.main()