import unittest

from impl.MerkleTree import *


def get_answer():
    with open('test/BaseTestAnswer') as f:
        return f.read()


def concat(x, y):
    return Hashing.reformat(x) + Hashing.reformat(y)


def base_test(tree: MerkleTreeInterface):
    res = [""]

    def record(s):
        res[0] += str(s) + "\n"

    for i in range(16):
        tree.add_message(chr(97 + i))
        record(tree)

    tree.update(0, '?')
    tree.update(8, '!')

    record(tree)
    record(tree.get_digest())
    record(tree.get_hash_of_item(9))

    record(type(tree)(message_list=list("Hello, world!"),
                      hash_algo='test', concat_method=concat))
    return res[0]


def verification_test(tree: MerkleTreeInterface):
    idx = 8

    path = tree.get_auth_path(idx)
    item_hash = tree.get_hash_of_item(idx)
    root = tree.get_digest()
    return verify_path(item_hash, path, root, tree.hash, tree.concat_method)


class MerkleTreeTest(unittest.TestCase):

    def test(self):
        tree = MerkleTree(hash_algo='test', concat_method=concat)
        print(base_test(tree))
        # self.assertEqual(base_test(tree), get_answer())
        self.assertTrue(verification_test(tree))


if __name__ == '__main__':
    unittest.main()
