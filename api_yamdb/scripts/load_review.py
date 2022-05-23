from reviews.models import Review

from csv import DictReader


def run():
    with open('static/data/review.csv', 'r',
              encoding='utf-8') as csvfile:
        csv_reader = DictReader(csvfile)
        Review.objects.all().delete()
        for row in csv_reader:
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date']
            )
            review.save()
