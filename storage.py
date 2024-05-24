import datetime
from hashlib import sha256

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase): pass


class UserData(Base):
    __tablename__ = "data"
    user_id: Mapped[str] = mapped_column(primary_key=True)
    data: Mapped[str]
    password: Mapped[str]
    last_modified: Mapped[int]


sqlite_database = "sqlite:///users.db"
engine = create_engine(sqlite_database)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine, autoflush=False)

dbsession = Session()


def get_user_data(user_id: str, password: str) -> str | None:
    got = dbsession.query(UserData).where(UserData.user_id == user_id).first()
    if sha256(password).hexdigest() == got.password:
        return got.data
    else:
        return None


def set_user_data(user_id: str, data: str, password: str) -> bool:
    got = dbsession.query(UserData).where(UserData.user_id == user_id).first()
    timespamp = int(datetime.datetime.now().timestamp())
    if not got:
        new_data = UserData(user_id=user_id, data=data, password=sha256(password).hexdigest(), last_modified=timespamp)
    else:
        if sha256(password).hexdigest() == got.password:
            new_data = got
            new_data.data = data
            new_data.last_modified = timespamp
        else:
            return False
    dbsession.add(new_data)
    dbsession.commit()
    return True