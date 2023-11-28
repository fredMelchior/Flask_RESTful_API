from models import People, User


def insert_people():
    people = People(name='Lula', age=495)
    print(people)
    people.save()


def consult_people():
    roberta = People.query.filter_by(name='Roberta').first()
    print(roberta)
    people = People.query.all()
    print(f"All People Registered in DB:\n{people}")


def alter_people():
    people = People.query.filter_by(name='Roberta').first()
    people.age = 43
    people.save()


def delete_people():
    people = People.query.filter_by(name="Lula").first()
    people.delete()


def insert_user(login, password):
    user = User(login=login, password=password)
    user.save()


def list_all_users():
    all_users = User.query.all()
    print(all_users)


if __name__ == '__main__':
    # insert_people()
    # consult_people()
    # alter_people()
    # delete_people()
    # insert_user('Lupita', '123456')
    # insert_user("Fred", "123456")
    list_all_users()
