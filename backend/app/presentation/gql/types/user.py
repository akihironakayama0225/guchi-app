import strawberry
from presentation.gql.types.boolean import BooleanType
from infrastructure.db.setting import session
from domain.entity.user import UserModel  # NOTE: strawberryのUser typeと名前衝突するため
from strawberry.dataloader import DataLoader
from typing import List
import datetime as dt

from presentation.gql.context import Info


# https://strawberry.rocks/docs/guides/dataloaders
# 渡されたキーのリストに基づいてユーザーのリストを返す関数を定義する必要があります
async def load_users(keys: List[int]) -> List[UserModel]:
    return session.query(UserModel).filter(UserModel.id.in_(keys))


@strawberry.type
class User:
    id: int
    nickname: str

    @classmethod
    def get_current_user(cls, info: Info):
        return info.context.current_user

    @classmethod
    async def get_users(cls, info: Info):
        if not info.context.current_user.is_admin:
            raise "User is not Admin."

        loader = DataLoader(load_fn=load_users)
        # users = await asyncio.gather(loader.load(1), loader.load(2), loader.load(3), loader.load(4))
        # loader.load(1)
        # loader.load(2)
        # loader.load(3)
        # loader.load(4)
        # print("USERS", users)
        users = session.query(UserModel).all()
        return users

    @classmethod
    def withdraw_current_user(cls, info: Info):
        try:
            user = info.context.current_user
            user.expired_at = dt.datetime.now()
            session.commit()
            return BooleanType(True)

        except Exception as e:
            session.rollback()
            print(e)
            return BooleanType(False)
        finally:
            session.close()
