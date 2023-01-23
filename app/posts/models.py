from django.db import models
from accounts.models import Author


class Post(models.Model):
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.user.username} -{self.publication_date}'

    def get_status(self):
        statuses = Status.objects.filter(post=self).values('status')
        result = {}
        num = 0
        ser = 0
        for i in statuses:
            num = num + i['status']
            ser = ser + 1
        if num != 0:
            result['оценка'] = num / ser
            return result
        result['оценка'] = num
        return result


class Comment(models.Model):
    text = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=55, blank=True, null=True, help_text="Временный аккаунт")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.user.username} - {self.post.id}'


class Status(models.Model):
    status = models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'author')

    def __str__(self):
        return self.status


