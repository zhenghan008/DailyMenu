import time
from models.menu_models import *
import datetime


class MenuController:

    # 获取指定前几天的菜单
    def get_someDaysAgo_menu(self, day=4):
        days = [(datetime.datetime.now() - datetime.timedelta(days=i)).date() for i in range(1, day + 1)]
        res = Dbsession.query(Dishes.name, Category.name, DailyMenu.create_date).filter(DailyMenu.dishes_id == Dishes.id).filter(DailyMenu.stapleFood_id == Category.id).filter(DailyMenu.create_date.between(days[-1], days[0])).all()

        print(res)


if __name__ == '__main__':
    MenuController().get_someDaysAgo_menu()
