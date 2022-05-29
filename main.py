import random

E = '71828182845904523536'

TEXT = """
    Князь Василий исполнил обещание, данное на вечере у Анны Павловны княгине Друбецкой, просившей его о своем
    единственном сыне Борисе. О нем было доложено государю, и, не в пример другим, он был переведен в гвардии
    Семеновский полк прапорщиком. 
"""

class HashTable:

    def __init__(self, size):
        self.size = size
        self.keys = [None] * self.size
        self.data = [None] * self.size

    def put(self, key, value):
        hash_value = self.hash_function(key, self.size)

        if self.keys[hash_value] is None:
            self.keys[hash_value] = key
            self.data[hash_value] = value

        else:
            if self.keys[hash_value] == key:
                self.data[hash_value] = value

            else:
                next_key = self.rehash(hash_value, self.size)

                while self.keys[next_key] is not None and self.keys[hash_value] is not key:
                    next_key = self.rehash(next_key, len(self.keys))

                if self.keys[next_key] is None:
                    self.keys[next_key] = key
                    self.data[next_key] = value

                else:
                    self.data[next_key] = value

    def hash_function(self, key, size):
        return key % size

    def rehash(self, old_hash, size):
        return (old_hash + 1) % size

    def get_capacity(self):
        keys = []
        for key in self.keys:
            if key is not None:
                keys.append(key)
        return (len(keys) / self.size) * 100

    def get(self, key):
        start_pos = self.hash_function(key, self.size)

        data = None
        stop = False
        found = False

        while self.keys[start_pos] is not None and not stop and not found:
            if self.keys[start_pos] == key:
                found = True
                value = self.data[start_pos]
            else:
                position = self.rehash(start_pos, self.size)
                if position == start_pos:
                    stop = True
                else:
                    position = self.rehash(position, self.size)
                    if position == start_pos:
                        stop = True

        return data

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __str__(self):
        keys = []
        values = []
        hash_list = []
        for key in self.keys:
            if key is not None:
                keys.append(key)
        for value in self.data:
            if value is not None:
                values.append(value)
        for i in range(len(keys)):
            hash_list.append((keys[i], values[i]))

        return f"{str(hash_list)}\n" \
               f"Capacity: {((len(keys) / self.size) * 100):.2f}%"

    def __repr__(self):
        pass


def get_permutation_table():
    table = [[] for i in range(20)]

    for i in range(20):
        for j in range(20):
            table[i].append(int(random.choice(E)))

    return table


def buble(old_size, permutation_table, factor=1):
    new_size = old_size * factor
    get_hash_of(TEXT, new_size, permutation_table)
    print(f"Buble {old_size} -> {new_size}")


def get_hash_of(text, size_of_hash_table, permutation_table, level_p_t=0):
    hash_table = HashTable(size_of_hash_table)
    sum = 0
    factor = 1
    for word in text.replace(",", "").replace(".", "").replace("!", "").replace("?", "").split():
        for i in range(len(word)):
            if len(word) < len(permutation_table) - 1:
                sum += ord(word[i]) * permutation_table[level_p_t][i]
            else:
                sum += ord(word[i]) * permutation_table[level_p_t][i % len(permutation_table)]
            sum = sum // len(word) % size_of_hash_table
        #if hash_table[sum] != word:
        hash_table[sum] = word
        if hash_table.get_capacity() > 95:
            #del hash_table
            factor *= 2
            buble(size_of_hash_table, permutation_table, factor)

    print(hash_table)


if __name__ == '__main__':

    get_hash_of(TEXT, 32, get_permutation_table())
