from .models import Pelis
from mongodbforms import DocumentForm
from mongodbforms import EmbeddedDocumentForm
from django.forms import TextInput, Textarea, NumberInput
from django.utils.translation import gettext_lazy as _

class PelisForm(DocumentForm):

	class Meta:

		model = Pelis
		fields = ["title","year","rated","runtime","director","plot","poster","metacritic", "type"]
		widgets = {"title": TextInput(attrs={"size":50,"class":"form-control"}),"rated":TextInput(attrs={"size":50,"class":"form-control"}), "director": TextInput(attrs={"size":50,"class":"form-control"}),"plot": Textarea(attrs={'cols': 50, 'rows': 4,"class":"form-control"}), "poster": TextInput(attrs={"size":50,"class":"form-control"}), "type":TextInput(attrs={"size":50,"class":"form-control"}),"year":NumberInput(attrs={"class":"form-control"}),"runtime":NumberInput(attrs={"class":"form-control"}),"metacritic":NumberInput(attrs={"class":"form-control"})}	
		
		
		
