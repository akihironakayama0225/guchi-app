from abc import ABCMeta, abstractmethod

# DI Container
from container import Container

from infrastructure.db.setting import session

from logging import getLogger
from utils.my_logger import FASTAPI_LOG

fastapi_logger = getLogger(FASTAPI_LOG)

class BaseUseCase(metaclass=ABCMeta):
    """DDDのUseCaseレイヤー

    UseCaseレイヤーは、アクターがエンティティに対して行うアクションを明示します。
    全てのUseCaseは、このクラスを継承する必要があります。
    """

    def __init__(self):
        self.session = session

    @abstractmethod
    def _execute(self):
        raise NotImplementedError

    def execute(self, *args, **kwargs):
        try:
            ret = self._execute(*args, **kwargs)
            session.commit()
            return ret
        except Exception as e:
            fastapi_logger.exception(e)
        finally:
            session.close()

    def resolve(self, interface):
        """指定したインターフェースに対応する実装を返す

        Args:
            interface (I_Repository): リポジトリのインターフェース

        Returns:
            Repository: リポジトリの実装
        """
        return Container().resolve(interface)
