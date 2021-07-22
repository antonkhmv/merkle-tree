from abc import ABC, abstractmethod
from typing import Callable, Any, List
import Hashing


class MerkleTreeInterface(ABC):

    def __init__(self,
                 hash_algo: str = 'sha256',
                 message_list: List = None,
                 concat_method: Callable[[Any, Any], Any] = lambda x, y: x + y):

        self.hash_algo = Hashing.get_hash_func(hash_algo)
        self.concat_method = concat_method
        self.message_list = message_list

    tree: Any

    def __str__(self):
        return str(self.tree)

    def hash(self, item):
        """
        !!Encode strings before using this method
        """
        return self.hash_algo(item).digest()

    @abstractmethod
    def add_message(self, item):
        pass

    @abstractmethod
    def update(self, position: int, item):
        pass

    @abstractmethod
    def verify(self, position: int, item_hash, path: List) -> bool:
        pass

    @abstractmethod
    def get_auth_path(self, position: int) -> List:
        pass

    @abstractmethod
    def get_hash_of_leaf(self, position):
        pass

    @abstractmethod
    def get_digest(self):
        pass
