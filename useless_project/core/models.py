from django.db import models


class Score(models.Model):
    username = models.CharField(max_length=30)
    seconds_wasted = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-seconds_wasted', 'created_at']
        verbose_name = 'Score'
        verbose_name_plural = 'Scores'

    def __str__(self):
        return f"{self.username} - {self.seconds_wasted:.2f}s"
