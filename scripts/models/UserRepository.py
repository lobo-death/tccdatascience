from scripts.models.models import User


class UserRepository:

    @staticmethod
    def find_by_id(id):
        return User.get(User.id == id)

    @staticmethod
    def create(users):
        for user in users:
            return User.create(**user)
