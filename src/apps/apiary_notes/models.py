from django.db import models

class ApiaryNote(models.Model):
    apiary = models.ForeignKey(
        'apiaries.Apiary',
        on_delete=models.CASCADE,
        related_name='notes'
    )
    date = models.DateField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'apiary_notes'
        db_table = 'apiary_notes'
        verbose_name = 'apiary note'
        verbose_name_plural = 'apiary notes'
        ordering = ['date']

    def __str__(self):
        return f'{self.apiary.name} - {self.date}'