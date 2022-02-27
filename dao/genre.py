from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, gen_id):
        return self.session.query(Genre).get(gen_id)

    def get_all(self):
        return self.session.query(Genre).all()

    def create(self, data):
        new_gen = Genre(**data)
        self.session.add(new_gen)
        self.session.commit()
        return new_gen

    def update(self, gen):
        self.session.add(gen)
        self.session.commit()

    def delete(self, gen_id):
        genre = self.get_one(gen_id)
        self.session.delete(genre)
        self.session.commit()
