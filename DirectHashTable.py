# Functions for prime number calculations, used for resizing the hash table efficiently.
# Source: https://stackoverflow.com/questions/60003330/find-the-next-prime-number-in-python
def is_prime(x):
    return all(x % i for i in range(2, x))


def next_prime(x):
    return min([a for a in range(x + 1, 2 * x) if is_prime(a)])


# Adapted from W-1_ChainingHashTable_zyBooks_Key-Value.py
# Implements a hash table using direct hashing.
class DirectHashTable:
    # Initializes the hash table with an optional initial capacity.
    def __init__(self, initial_capacity=40):
        # Creates an empty hash table with the specified capacity.
        self.table = [None] * initial_capacity

    # Inserts a key-value pair into the hash table.
    def insert(self, key, item):
        # Determines the appropriate bucket for storing the item.
        bucket = hash(key) % len(self.table)
        key_value = [key, item]

        # If the bucket is empty, store the new key-value pair.
        if self.table[bucket] is None:
            self.table[bucket] = key_value
        # If the key already exists in the bucket, update its value.
        elif self.table[bucket][0] == key:
            self.table[bucket][1] = item
        # If a collision occurs, resize the table and retry insertion.
        else:
            self.hash_resize(len(self.table))
            self.insert(key, item)
        return True

    # Searches for a key in the hash table.
    # Returns the associated value if found, otherwise returns None.
    def search(self, key):
        # Determines the bucket where the key should be located.
        bucket = hash(key) % len(self.table)
        key_value = self.table[bucket]

        # If the bucket is empty, the key does not exist.
        if key_value is None:
            return None
        # If the key is found, return its corresponding value.
        else:
            return key_value[1]

    # Removes a key-value pair from the hash table.
    def remove(self, key):
        # Finds the bucket for the key and removes its contents.
        bucket = hash(key) % len(self.table)
        self.table[bucket] = None

    # Implements hash table resizing based on pseudocode from
    # C949: Data Structures and Algorithms I (15.6: Hash Table Resizing).
    def hash_resize(self, cur_size):
        # Doubles the current table size and finds the next prime number
        # to use as the new table size.
        new_size = next_prime(cur_size * 2)
        new_array = DirectHashTable(new_size)

        bucket = 0
        # Rehashes all existing key-value pairs into the new table.
        while bucket < cur_size:
            key_value = self.table[bucket]
            if key_value is not None:
                new_array.insert(key_value[0], key_value[1])
            bucket += 1

        # Replaces the old table with the resized one.
        self.table = new_array.table
