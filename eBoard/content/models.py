from django.contrib.auth.models import User
from django.db import models


class Announce(models.Model):
	CATEGORY = (
		('tanks', 'Танки'),
		('heals', 'Хилы'),
		('dd', 'ДД'),
		('sellers', 'Торговцы'),
		('guildmasters', 'Гильдмастера'),
		('questgivers', 'Квестгиверы'),
		('smiths', 'Кузнецы'),
		('tanners', 'Кожевники'),
		('potionmakers', 'Зельевары'),
		('spellmasters', 'Мастера заклинаний'),
	)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=64)
	text = models.TextField()
	category = models.CharField(max_length=16, choices=CATEGORY, default='tanks')
	dateCreation = models.DateTimeField(auto_now_add=True)
	upload = models.FileField(upload_to='uploads/', blank=True)

	def __str__(self):
		return f'{self.author}: {self.title}'

	def get_absolute_url(self):
		return f'/announce/{self.id}'


class UserReaction(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	announce = models.ForeignKey(Announce, on_delete=models.CASCADE, related_name='reactions')
	dateCreation = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=False)

	def __str__(self):
		return 'Reaction by {} on {}'.format(self.author, self.announce)

	def get_absolute_url(self):
		return f'/reacts/{self.id}'
