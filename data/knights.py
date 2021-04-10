import sqlalchemy as sa
from .db_session import SqlAlchemyBase

class Knight(SqlAlchemyBase):
    __tablename__ = 'knight'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    enemy = sa.Column(sa.String, nullable=True)
    enemyhp = sa.Column(sa.Integer, nullable=True)
    shield = sa.Column(sa.Integer, nullable=True)
    minatack = sa.Column(sa.Integer, nullable=True)
    maxatack = sa.Column(sa.Integer, nullable=True)
    firstkill = sa.Column(sa.String, nullable=True)
    secondkill = sa.Column(sa.String, nullable=True)
    thirdkill = sa.Column(sa.String, nullable=True)
    number = sa.Column(sa.Integer, nullable=True)