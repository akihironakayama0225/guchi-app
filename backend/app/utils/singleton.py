from abc import ABCMeta, abstractmethod


class Singleton(metaclass=ABCMeta):
    """シングルトンの抽象クラス"""

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
