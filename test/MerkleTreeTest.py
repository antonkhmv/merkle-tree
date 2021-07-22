import unittest

from impl.MerkleTree import *


def get_answer():
    with open('test/BaseTestAnswer') as f:
        return f.read()


def test_concat(x, y):
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
    record(tree.get_hash_of_leaf(9))

    record(type(tree)(message_list=list("Hello, world!"),
                      hash_algo='test', concat_method=test_concat))
    return res[0]


def verification_test():

    l1 = list(map(lambda x: x.encode('utf-8'), "ABCDEFGHIJKLMNOP"))
    l2 = list(map(lambda x: x.encode('utf-8'), "CBCDGFGGHLKLMOOP"))

    t1 = MerkleTree(message_list=l1, hash_algo='sha256')

    t2 = MerkleTree(message_list=l2,  hash_algo='sha256')

    errors = ''

    for i in range(len(l1)):
        r1 = t1.verify(t2.get_hash_of_leaf(i), i)
        r2 = t2.verify(t1.get_hash_of_leaf(i), i)

        if r1 != r2:
            return False

        errors += ('1' if r1 else '0')

    return errors == ''.join(map(lambda x: '1' if x[0] == x[1] else '0', zip(l1, l2)))


class MerkleTreeTest(unittest.TestCase):

    def test(self):
        tree = MerkleTree(hash_algo='test', concat_method=test_concat)
        self.assertEqual(base_test(tree), get_answer())
        self.assertTrue(verification_test())


if __name__ == '__main__':
    unittest.main()
