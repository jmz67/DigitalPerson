from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        else:
            # 将访问的键移到最前面
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # 更新值并将键移到最前面
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # 移除最久未使用的项
            self.cache.popitem(last=False)


if __name__ == '__main__':
    # 测试用例
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))  # 返回 1
    cache.put(3, 3)      # 该操作会使得键 2 被移除
    print(cache.get(2))  # 返回 -1 (未找到)
    cache.put(4, 4)      # 该操作会使得键 1 被移除
    print(cache.get(1))  # 返回 -1 (未找到)
    print(cache.get(3))  # 返回 3
    print(cache.get(4))  # 返回 4