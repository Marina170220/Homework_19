from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, gen_id):
        return self.dao.get_one(gen_id)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        genre = self.get_one(data.get("id"))
        if genre:
            genre.name = data.get("name")
            return self.dao.update(data)
        return None

    def delete(self, gen_id):
        return self.dao.delete(gen_id)
