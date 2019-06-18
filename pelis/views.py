from django.shortcuts import render, redirect
from . import models
from . import forms
from mongoengine import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from .serializers import PelisSerializer
from rest_framework.parsers import JSONParser
import json

# Importar biblioteca loegging.
import logging

# Obtener el logger
logger = logging.getLogger(__name__)

# Función que renderiza la página principal de la aplicación.
def home(request):

	return(render(request,"pelis/index.html",{}))

	
# Función para realizar una consulta sobre la base de datos de mongo con mongoengine.
# Devuelve todas las películas que pertenezcan al género indicado como argumento.
@login_required
def consultaGenero(request,genero):

	# Realizamos la consulta.
	peliculas = models.Pelis.objects(genres=genero)

	# Empaquetamos los resultados.
	context = {"tipoConsulta":"genero","consulta":genero,"peliculas":[]}

	for p in peliculas:

		context["peliculas"].append({"title":p.title,"year":p.year})

	return(render(request,"pelis/consultas.html",context))

# Función para realizar una consulta sobre la base de datos de mongo con mongoengine.
# Devuelve todas las películas que hayan sido dirigidas por el director indicado como argumento.
@login_required
def consultaDirector(request,director):

	# Realizamos la consulta.
	peliculas = models.Pelis.objects(director=director)

	# Empaquetamos los resultados.
	context = {"tipoConsulta":"director","consulta":director,"peliculas":[]}

	for p in peliculas:

		context["peliculas"].append({"title":p.title,"year":p.year})

	return(render(request,"pelis/consultas.html",context))

# Función para realizar una consulta sobre la base de datos de mongo con mongoengine.
# Devuelve todas las películas que hayan sido estrenadas en el año indicado como argumento.
@login_required
def consultaAnio(request,anio):

	# Realizamos la consulta.
	peliculas = models.Pelis.objects(year=anio)

	# Empaquetamos los resultados.
	context = {"tipoConsulta":"año","consulta":anio,"peliculas":[]}

	for p in peliculas:

		context["peliculas"].append({"title":p.title,"year":p.year})

	return(render(request,"pelis/consultas.html",context))

# Función para mostrar el formulario de consulta.
@login_required
def consulta(request):

	# Obtenemos una lista con los títulos de todas las películas
	# para realizar el typeahead.
	lista_peliculas = ""
	for p in models.Pelis.objects:

		lista_peliculas += "\"{}\",\n".format(p['title'])

	return(render(request,"pelis/formulario_consulta.html",{"listaPeliculas":lista_peliculas[:-2]}))


# Función para realizar una consulta sobre la base de datos de mongo con mongoengine.
# Devuelve todas las películas el las que haya participado el actor recibido como argumento.
@login_required
def resultadoConsulta(request):

	# Obtener el criterio de consulta.
	criterio = request.GET.get("criterio")
	peliculas = []
	context = {}

	if(criterio == "titulo"):
		
		# Realizamos la consulta.
		peliculas = models.Pelis.objects(title__icontains=request.GET.get("busqueda"))
		
		# Empaquetamos los resultados.
		context = {"tipoConsulta":"titulo","consulta":request.GET.get("busqueda"),"peliculas":[]}

	elif(criterio == "anio"):
		
		# Realizamos la consulta.
		peliculas = models.Pelis.objects(year=request.GET.get("busqueda"))
		
		# Empaquetamos los resultados.
		context = {"tipoConsulta":"anio","consulta":request.GET.get("busqueda"),"peliculas":[]}

	elif(criterio == "actor"):
		
		# Realizamos la consulta.
		peliculas = models.Pelis.objects(actors=request.GET.get("busqueda"))
		
		# Empaquetamos los resultados.
		context = {"tipoConsulta":"actor","consulta":request.GET.get("busqueda"),"peliculas":[]}

	elif(criterio == "genero"):
		
		# Realizamos la consulta.
		peliculas = models.Pelis.objects(genres=request.GET.get("busqueda"))
		
		# Empaquetamos los resultados.
		context = {"tipoConsulta":"género","consulta":request.GET.get("busqueda"),"peliculas":[]}

	elif(criterio == "director"):
		
		# Realizamos la consulta.
		peliculas = models.Pelis.objects(director__icontains=request.GET.get("busqueda"))
		
		# Empaquetamos los resultados.
		context = {"tipoConsulta":"director","consulta":request.GET.get("busqueda"),"peliculas":[]}	

	for p in peliculas:

		context["peliculas"].append({"id":str(p.id),"title":p.title,"year":p.year,"genres":p.genres,"director":p.director,})

	return(render(request,"pelis/tabla_actor.html",context))

# Función para mostrar la información de una película concreta cuyo id de la base de datos de
# mongo se recibe como argumento.
@login_required
def info_de(request,id):

	# Realizamos la consulta.
	p = models.Pelis.objects.get(id=id)

	# Si la película no tiene el comao likes inicializado,
	# ponerlo a 0. 
	if(p.likes == None):

		models.Pelis.objects(id=id).update_one(set__likes=0)
		p.reload()
		
	# Empaquetamos el resultado.
	context = p.to_mongo().to_dict()

	# Pasar las listas a cadenas de caracteres.
	for k in context:

		if(type(context[k]) == list):
			
			cadena = ""	
			for i in context[k]:

				cadena += str(i) + ", "
			
			cadena = cadena[:-2]
			cadena += "."
			context[k] = cadena
		

	if("poster" not in context.keys()):

		context["poster"] = None

	if(context["poster"] != None):

		context["poster"] = "https://m.media-amazon.com/" + context["poster"][25:]

	context["id"] = id
	return(render(request,"pelis/info_de.html",context))

# Función para añadir una película nueva a la base de datos.
@staff_member_required
def crear_pelicula(request):

	if(request.method =="POST"):

		form = forms.PelisForm(request.POST)

		if(form.is_valid()):

			form.save()
			return(redirect("/peliculas/"))
	else:

		form = forms.PelisForm()

	return(render(request,"pelis/editar_peli.html",{"form":form,"crear":True}))

# Función para editar una película de la base de datos identificada por su id.
@staff_member_required
def editar_pelicula(request,id):

	# Obtenemos la película.
	p = models.Pelis.objects.get(id=id)

	if(request.method =="POST"):

		form = forms.PelisForm(request.POST,instance=p)

		if(form.is_valid()):

			form.save()
			return(redirect("/peliculas/id/" + id))
	else:

		form = forms.PelisForm(instance=p)

	return(render(request,"pelis/editar_peli.html",{"form":form,"crear":False}))

# Función para eliminar una película de la base de datos identificada por su id.
@staff_member_required
def eliminar_pelicula(request,id):

	# Obtenemos la película.
	p = models.Pelis.objects.get(id=id)

	# Eliminamos la película.
	p.delete()

	return(redirect("/peliculas/peliculaEliminada"))

# Función que renderiza el resultado de eliminar una película.
@staff_member_required
def pelicula_eliminada(request):

	return(render(request,"pelis/pelicula_eliminada.html",{}))

# Función para actualizar el número de likes de una película.
@csrf_exempt
def actualizar_likes(request):

	if(request.method == "POST"):

		# Recuperamos la película cuyo número de likes se va a actualizar.
		p = models.Pelis.objects.get(id=request.POST.get("id"))

		# Actualizamos el número de likes.
		models.Pelis.objects(id=request.POST.get("id")).update_one(set__likes=(p.likes+int(request.POST.get("like"))))
		p.reload()
		
		# Devolvemos el nuevo número de likes de la película.
		return JsonResponse({'likes':p.likes})

# Función del API REST para obtener todas las películas o para añadir una nueva.
@csrf_exempt
def api_pelis(request):

	# Si se recibe una petición GET, devolvemos todas las películas.
	if(request.method == "GET"):

		serializer = PelisSerializer(models.Pelis.objects.all(),many = True)
		return(JsonResponse(serializer.data, safe = False))

	# Si se recibe una petición POST, entonces es que se va a añadir una película 
	# a la base de datos.
	if(request.method == "POST"):

		data = JSONParser().parse(request)
		serializer = PelisSerializer(data=data)

		if(serializer.is_valid()):

			serializer.save()
			return JsonResponse(serializer.data, status = 201)


	logger.debug("Error")
	return(JsonResponse(serializer.errors,status = 400))

# Función del API REST para consultar, modificar o borrar un película concreta.
@csrf_exempt
def api_peli(request,id):

	try:

		p = models.Pelis.objects.get(id=id)

	except:

		logger.debug("Error, película no encontrada.")
		return HttpResponse(status=404)

	# Si se recibe una petición GET, devolvemos la película en formato json.
	if(request.method == "GET"):
		
		serializer = PelisSerializer(p)
		return(JsonResponse(serializer.data))

	# Si se recibe una petición PUT, modificamos la película con los parámetros
	# recibidos por el usuario en formato json.
	if(request.method == "PUT"):

		data = JSONParser().parse(request)
		serializer = PelisSerializer(p, data=data)

		if(serializer.is_valid()):

			serializer.save()
			return(JsonResponse(serializer.data,status=200))

		return JsonResponse(serializer.errors, status=400)

	# Si se recibe una petición DELETE, borramos de la base de datos la película
	# cuyo id recibimos como argumento.
	if(request.method == "DELETE"):

		p.delete()
		return(HttpResponse(status=204))
