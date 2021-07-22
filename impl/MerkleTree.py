from MerkleTreeInterface import *


def verify_path(
        item_hash,
        path,
        root,
        hash_func,
        concat_method):
    for h, direction in path:

        if direction:
            o1, o2 = h, item_hash
        else:
            o1, o2 = item_hash, h

        item_hash = hash_func(concat_method(o1, o2))

    return root == item_hash


class MerkleTree(MerkleTreeInterface):
    """
    A data structure for efficient hash verification
    Updating time complexity: O(log n)
    Verification time complexity: O(log n)
    Adding a new message time complexity: O(1)
    Memory complexity: O(n)
    """

    def __init__(self,
                 hash_algo: str = 'sha256',
                 message_list: List = None,
                 concat_method: Callable[[Any, Any], Any] = lambda x, y: x + y):
        """
        :param hash_algo: The algorithm used for hashing. Return type has to have __add__ overloaded
        :param message_list: The list of messages to initialize the tree with.
        :param concat_method: The method for concatenating hashes together
        """
        super().__init__(hash_algo, message_list, concat_method)
        self.size = 0

        # n - the size of the tree; m - a half of the size of the tree.
        self.n = 1
        self.m = 0

        self.tree = [bytes()]

        if self.message_list is not None:
            from math import log2, ceil

            self.size = len(self.message_list)
            self.m = pow(2, ceil(log2(self.size)))
            self.n = self.m >> 1
            self.rebuild_tree(message_list)

    def rehash_single(self, position: int):
        """
        Rehashes all the ancestors of the node at index = position.
        :param position: the position of the hash to be rehashed
        """
        while position > 1:
            # "x & -2" makes the last bit of 'x' a 0, "x | 1" -- a 1
            p1, p2 = position & -2, position | 1

            position >>= 1

            self.tree[position] = self.hash(self.concat_method(self.tree[p1], self.tree[p2]))

    def rehash_all(self, position: int):
        """
        Rehashes all the children of the node at index = position
        """
        if position >= len(self.tree):
            return None
        if position >= len(self.tree) >> 1:
            return self.tree[position]

        h1, h2 = self.rehash_all(position << 1), self.rehash_all(1 + (position << 1))
        res = self.hash(self.concat_method(h1, h2))
        self.tree[position] = res
        return res

    def rebuild_tree(self, new_leaves, leaves_hashed=False):
        """
        Rebuilds the tree with a new 'leaves' array
        :param new_leaves: the array for rebuilding the tree
        :param leaves_hashed: whether the array contains the items or the hashes of the items
        """

        if not leaves_hashed:
            new_leaves = list(map(self.hash, new_leaves))

        if self.size == 1:
            self.tree = [bytes()] + new_leaves
        else:
            self.size = len(new_leaves)
            self.tree = self.m * [bytes()] + new_leaves + (self.m - self.size) * [bytes()]
            self.rehash_all(1)

    def add_message(self, item):
        """
        Add an item to the merkle tree
        !!Encode before using this method
        :param item: value of a new item
        """

        h = self.hash(item)

        self.size += 1

        if self.size > self.m:
            s = self.n - self.m
            self.n *= 2
            self.m = self.n >> 1
            self.rebuild_tree(self.tree[s:] + [h], leaves_hashed=True)
        else:
            self.tree[self.m + self.size - 1] = h
            self.rehash_single(self.m + self.size - 1)

    def update(self, position: int, item):
        """
        Update the value of an item and rehash all updated nodes in the tree
        :param position: the position of the item
        :param item: the new value of the item
        """
        position += len(self.tree) >> 1
        self.tree[position] = self.hash(item)
        self.rehash_single(position)

    def get_digest(self):
        """
        :return: The root of the tree
        """
        return self.tree[1]

    def get_hash_of_leaf(self, position):
        """
        :param position: the position of the requested item in the leaves array
        :return: the leaf hash of an item requested
        """
        position += self.m
        return self.tree[position]

    def verify(self, item_hash, position, path=None):
        """
        Verify that digest matches the source via an item and the path
        :param item_hash:
        :param position: the position of the leaf to verify
        :param path: the list of hashes of parent and sibling nodes with their position with respect to the given item (left/right)
        :return:
        """

        if path is None:
            path = self.get_auth_path(position)

        #item_hash = self.get_hash_of_leaf(position)

        for h, direction in path:

            if direction:
                o1, o2 = h, item_hash
            else:
                o1, o2 = item_hash, h

            item_hash = self.hash(self.concat_method(o1, o2))

        return self.get_digest() == item_hash

    def get_auth_path(self, position: int) -> List:
        """
        :param position: the
        :return: the path for hash authentication (and direction for each node).
                 direction is 0 if the node is to the left and 1 if it's to the right
        """
        c = self.m
        position += self.m

        path = []

        while c > 1:
            path.append((self.tree[position ^ 1], position & 1))
            position >>= 1
            c >>= 1

        return path
