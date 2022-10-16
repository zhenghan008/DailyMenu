from sqlalchemy import Column, Integer, String, ForeignKey, Date

from models.db_util import Base, Session

Dbsession = Session()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def __repr__(self):
        return str({
            'id': self.id,
            'name': self.name
        })


class Dishes(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    category_id = Column(Integer, ForeignKey('category.id'))

    def __repr__(self):
        return str({
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id
        })


class DailyMenu(Base):
    __tablename__ = 'dailyMenu'
    id = Column(Integer, primary_key=True)
    dishes_id = Column(Integer, ForeignKey('dishes.id'))
    create_date = Column(Date)

    def __repr__(self):
        return str({
            'id': self.id,
            'dishes_id': self.dishes_id,
            'date': self.create_date
        })
