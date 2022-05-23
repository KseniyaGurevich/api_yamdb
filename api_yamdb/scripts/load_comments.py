from reviews.models import Comment

from csv import DictReader


def run():
    with open('static/data/comments.csv', 'r',
              encoding='utf-8') as csvfile:
        csv_reader = DictReader(csvfile)
        Comment.objects.all().delete()
        for row in csv_reader:
            comment = Comment(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date']
            )
            comment.save()
