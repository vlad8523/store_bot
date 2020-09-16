from TransformFunctions import create_storage

class Storage:
    ___shared_state = {}

    def __init__(self):
        self.__dict__ = self.___shared_state
        self.sizes_list = []
        self.storage_list = []

    def create_storage(self,raw_storage):
        self.storage_list = create_storage(raw_storage)

    def create_sizes(self):
        sizes_list = []
        for item in self.storage_list:
            sizes_list.append(item['sizes'])

    def get_storage(self):
        return self.storage_list

    def get_sizes(self):
        return self.sizes_list
