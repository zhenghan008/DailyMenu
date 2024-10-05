import random
from models.menu_models import *
import datetime


class MenuController:

    def __init__(self, day=4, dishes_num=2, staple_food_id=1):
        self.dishes_num = dishes_num
        self.staple_food_id = staple_food_id
        self.now = datetime.datetime.now()
        self.tomorrow = (self.now + datetime.timedelta(days=1)).date()
        self.days = [(self.now - datetime.timedelta(days=i)).date() for i in range(1, day + 1)]
        self.days.append(self.now.date())

    # 获取指定前几天的菜单
    def get_someDaysAgo_menu_ids(self):
        res = Dbsession.query(DailyMenu.dishes_id, Dishes.category_id).filter(DailyMenu.dishes_id == Dishes.id).filter(
            Dishes.category_id == Category.id).filter(
            DailyMenu.create_date.between(self.days[-1], self.days[0])).all()
        return res

    def get_chosen_menu(self, category_dishes_map):
        result = []
        optional_category_ids = [i for i in tuple(category_dishes_map.keys()) if i != 5]
        while 1:
            chosen_category = random.choices(optional_category_ids,
                                             weights=[1 for _ in range(len(optional_category_ids))],
                                             k=self.dishes_num)
            if len(set(chosen_category)) == self.dishes_num:
                break
        if self.staple_food_id == 1:
            chosen_category.append(5)
        # print(f"chosen_category {chosen_category}")
        not_choice_ids = [each for i in chosen_category for each in category_dishes_map[i]]
        if not_choice_ids:
            optional_dishes = Dbsession.query(Dishes.id, Dishes.name, Category.id, Category.name).filter(
                Dishes.category_id == Category.id).filter(
                Category.id.in_(tuple(chosen_category))).filter(Dishes.id.notin_(tuple(not_choice_ids))).all()
        else:
            optional_dishes = Dbsession.query(Dishes.id, Dishes.name, Category.id, Category.name).filter(
                Dishes.category_id == Category.id).filter(
                Category.id.in_(tuple(chosen_category))).all()
        for each_category in chosen_category:
            optional_list = []
            for res in optional_dishes:
                if res[2] == each_category:
                    optional_list.append(((res[-1], res[1]), (res[2], res[0])))
            result.append(random.choice(optional_list))
        return result

    def gen_menu(self):
        cate_ids = []
        try:
            someDaysAgo_menus = self.get_someDaysAgo_menu_ids()
            if self.staple_food_id == 1:
                cate_ids = [res[0] for res in Dbsession.query(Category.id).filter(Category.id.notin_((1,))).all()]
            elif self.staple_food_id == 2:
                cate_ids = [res[0] for res in
                            Dbsession.query(Category.id).filter(Category.id.notin_((1, 5))).all()]
            category_dishes_map = {each: {i[0] for i in someDaysAgo_menus if i[-1] == each} for each in cate_ids}
            # print(category_dishes_map)
            chosen_menu = self.get_chosen_menu(category_dishes_map)
            # print(chosen_menu)
            add_objs = [DailyMenu(dishes_id=each[-1][-1], create_date=self.tomorrow) for each in chosen_menu]
            del_res = Dbsession.query(DailyMenu.id).filter(DailyMenu.create_date == self.tomorrow).all()
            if del_res:
                delete_stmt = DailyMenu.__table__.delete().where(DailyMenu.id.in_(tuple([i[0] for i in del_res])))
                Dbsession.execute(delete_stmt)
            Dbsession.bulk_save_objects(add_objs)
        except Exception as e:
            Dbsession.rollback()
            return 0, f"GEN ERROR: {str(e)}"
        else:
            Dbsession.commit()
            return 1, f"GEN SUCCESS!result:{chosen_menu}"
        finally:
            Dbsession.close()


if __name__ == '__main__':
    print(MenuController().gen_menu())
