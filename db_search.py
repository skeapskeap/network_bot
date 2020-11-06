from sqlalchemy.orm import sessionmaker
from db_init import engine, SwList
from transliterate import translit

Session = sessionmaker(bind=engine)
session = Session()


def search_in_db(query_string: str) -> str:
    query_string = translit(query_string, 'ru', reversed=True)
    words = query_string.split()
    result = session.query(SwList)

    for word in words:
        result = result.filter(SwList.name.like(f'%{word}%'))

    if not result.all():
        return 'Ничего не найдено'
    if len(result.all()) >= 20:
        return 'Слишком много результатов. Уточните запрос'
        
    pretty_list = [f'{item.name} {item.ip}' for item in result.all()]
    pretty_string = '\n'.join(pretty_list)
    return pretty_string


if __name__ == '__main__':
    row = 'нарым 19'
    print(search_in_db(row))
