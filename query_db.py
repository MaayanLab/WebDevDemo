from app.model import Synonym, Tissue

# tissue = Tissue.query.first()
# print(tissue)

# blood = Tissue.query.filter_by(label='blood').first()
# print(blood)

# whole_blood = Synonym.query.filter_by(synonym='whole blood').all()
# print(whole_blood[0].tissue.label)

# userList = users.query\le
#     .join(friendships, users.id==friendships.user_id)\
#     .add_columns(users.userId, users.name, users.email, friends.userId, friendId)\
#     .filter(users.id == friendships.friend_id)\
#     .filter(friendships.user_id == userID)\
#     .paginate(page, 1, False)

tissues = Tissue.query\
    .outerjoin(Synonym, Synonym.tissue_id==Tissue.uuid)\
    .filter((Synonym.synonym == "skin melanocyte") | (Tissue.label == "skin melanocyte"))\
    .all()
print(len(tissues))
print(tissues[0].definition)
