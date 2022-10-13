from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

work_path = os.path.abspath(os.path.dirname(__file__)).replace("\\models", "")

Base = declarative_base()
engine = create_engine(f'sqlite:///{work_path}/database/menu.db', echo=True)

Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    # 创建表,如果不存在的话
    Base.metadata.create_all(engine)

