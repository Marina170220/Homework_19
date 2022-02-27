from dao.model.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, dir_id):
        return self.session.query(Director).get(dir_id)

    def get_all(self):
        return self.session.query(Director).all()

    def create(self, data):
        new_dir = Director(**data)
        self.session.add(new_dir)
        self.session.commit()
        return new_dir

    def update(self, dir):
        self.session.add(dir)
        self.session.commit()
        return dir

    def delete(self, dir_id):
        director = self.get_one(dir_id)
        self.session.delete(director)
        self.session.commit()


