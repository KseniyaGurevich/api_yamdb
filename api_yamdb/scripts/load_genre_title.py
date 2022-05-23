from reviews.models import GenreTitle

from csv import DictReader


def run():
    with open('static/data/genre_title.csv', 'r',
              encoding='utf-8') as csvfile:
        csv_reader = DictReader(csvfile)
        for row in csv_reader:
            genre_title = GenreTitle(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            genre_title.save()
