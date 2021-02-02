class UserStruct:
    def __init__(self, users = {}, count = 0):
        self.users = users
        self.count = count

    def add_user(self, firstname, lastname, patronymic):
        temp_id = self.count
        user = {"id": temp_id, "firstname": firstname, "lastname": lastname, "patronymic": patronymic}
        self.users[self.count] = user
        self.count += 1
        return self.users[temp_id]

    def get_all_users(self):
        user_list = []
        for key in self.users:
            user_list.append(self.users[key])
        return user_list

    def get_user_by_id(self, id):
        try:
            return self.users[id]
        except KeyError:
            return {"message": "id is not found"}

    def change_user(self, id, firstname, lastname, patronymic):
        try:
            user = self.get_user_by_id(id)
            user['firstname'] = firstname
            user['lastname'] = lastname
            user['patronymic'] = patronymic
            return user
        except KeyError:
            return {"message": "id is not found"}

    def delete_user(self, id):
        try:
            return self.users.pop(id)
        except KeyError:
            return {"message": "id is not found"}

    def delete_all(self):
        self.users = {}
        self.user_list = []
        return {"message": "all delete"}

db = UserStruct()
db.add_user("ew", "aweaw", "gf43")
db.add_user("jgt", "jyttn", "jjgy6")
print(db.get_all_users())
db.delete_user(1)
print(db.get_all_users())