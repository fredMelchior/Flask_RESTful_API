from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base


engine = create_engine('sqlite:///activities.db')

db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class People(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)
    age = Column(Integer)

    def __repr__(self):
        return f"<People ID number: {self.id}\n First name: {self.name}\t Age: {self.age}\n>"

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Activities(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    people_id = Column(Integer, ForeignKey('people.id'))
    people = relationship('People')

    def __repr__(self):
        return f"<Activity ID number: {self.id}\n Task: {self.name}\t Owner: {self.people_id.name}\n>"

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(20))

    def __repr__(self):
        return f"User: {self.login} ID: {self.id}\n"

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
