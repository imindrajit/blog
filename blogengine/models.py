from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
# Create your models here.


class Post(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=200, unique = True)
	url = models.SlugField(max_length=40, unique=True)
	pub_date = models.DateTimeField(default=timezone.now)
	views = models.IntegerField(default=0)
	body = models.TextField()

	class Meta:
		ordering = ["-pub_date"]

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return "/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.url)


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)

	def __unicode__(self):
		return self.user.username

