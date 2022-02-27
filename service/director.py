from dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, dir_id):
        return self.dao.get_one(dir_id)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        director = self.get_one(data.get("id"))
        if director:
            director.name = data.get("name")
            return self.dao.update(data)
        return None

    def delete(self, dir_id):
        return self.dao.delete(dir_id)



