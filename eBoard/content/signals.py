from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .views import UserReaction
from eBoard.eBoard import settings


@receiver(post_save, sender=UserReaction)
def notify_about_react(sender, instance, **kwargs):
	if kwargs['created']:
		announce_author_email = instance.announce.author.email
		subject, from_email, to = 'New React', 'example@yandex.ru', announce_author_email

		html_content = render_to_string(
			'react_created.html',
			{
				'text': f'{instance.text}',
				'link': f'{settings.SITE_URL}/reacts/{instance.pk}'
			}
		)

		msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
