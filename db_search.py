from sqlalchemy.orm import sessionmaker
from db_init import engine, SwList

Session = sessionmaker(bind=engine)
session = Session()


def search_in_db(keywords: list):
    result = session.query(SwList)
    for word in keywords:
        result = result.filter(SwList.name.like(f'%{word}%'))
    if len(result.all()) >= 20:
        return ['Слишком много результатов. Уточните запрос']
    pretty_list = [f'{item.name} {item.ip}' for item in result.all()]
    return pretty_list


if __name__ == '__main__':
    row = 'tolm 27'
    words = row.split()
    print(search_in_db(words))
