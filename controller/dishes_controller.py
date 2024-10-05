from models.menu_models import Dishes, Dbsession


def add_dishes(dishes_name, category_id):
    try:
        Dbsession.add(Dishes(name=dishes_name, category_id=category_id))
    except Exception as e:
        Dbsession.rollback()
        return 0, f"ADD ERROR: {str(e)}"
    else:
        Dbsession.commit()
        return 1, f"ADD SUCCESS!"
    finally:
        Dbsession.close()
