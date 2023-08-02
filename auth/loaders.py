from models.User import User
from app import login_manager

@login_manager.user_loader
def load_user(uid):
    if not uid or uid == "None":
        return None
    return User.query.get(int(uid))


"""
@login_manager.user_loader
def load_user(user):
    sess = Session()
    res = sess.query(User).filter_by(
        id=user
    ).first()
    sess.close()
    return res
"""
