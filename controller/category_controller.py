from models.menu_models import Category, Dbsession


def get_category():
    res = Dbsession.query(Category.id, Category.name).filter(Category.id != 1).all()
    return res
