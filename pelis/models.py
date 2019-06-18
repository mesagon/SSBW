from django.db import models
import mongoengine


# Nos conectamos a la base de datos.
mongoengine.connect("movies",host = "mongo", port = 27017)

class Pelis(mongoengine.Document):

	title     = mongoengine.StringField(required=True)
	year      = mongoengine.IntField(min_value=1900)
	rated     = mongoengine.StringField()
	runtime   = mongoengine.IntField()
	countries = mongoengine.ListField(mongoengine.StringField())
	genres = mongoengine.ListField(mongoengine.StringField())
	director = mongoengine.StringField()
	writers = mongoengine.ListField(mongoengine.StringField())
	actors = mongoengine.ListField(mongoengine.StringField())
	plot = mongoengine.StringField()
	poster = mongoengine.StringField()
	imdb = mongoengine.DictField()
	tomato = mongoengine.DictField()
	metacritic = mongoengine.IntField()
	awards = mongoengine.DictField()
	type = mongoengine.StringField()
	likes = mongoengine.IntField()
