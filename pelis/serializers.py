from rest_framework_mongoengine import serializers
from .models import Pelis

class PelisSerializer(serializers.DocumentSerializer):

	class Meta:

		model = Pelis
		fields = '__all__'
