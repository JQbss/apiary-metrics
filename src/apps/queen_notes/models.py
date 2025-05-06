from django.db import models


class QueenNote(models.Model):
    queen = models.ForeignKey(
        'queens.Queen',
        on_delete=models.CASCADE,
        related_name='notes'
    )
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        app_label = 'queen_notes'
        db_table = 'queen_notes'
        verbose_name = 'queen note'
        verbose_name_plural = 'queen notes'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.queen.hive.apiary.name} - {self.queen.hive.name} - {self.created_at}'
