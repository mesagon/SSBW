from django.shortcuts import render
from django.shortcuts import HttpResponse
import random as r
import re
import requests
from pymongo import MongoClient

def hola_mundo(request, usuario):

	salida = """
		<html>
   		
  			Hola """ + usuario + """ 
		
		</html> """

	return(HttpResponse(salida))

# Ejercicio: Given a list of numbers, find and print all the list elements with an even index number. (i.e. A[0], A[2], A[4], ...).
def posiciones_pares(request):

	lista = [0,1,2,3,4,5,6,7,8,9]

	salida = """<html>

			Elementos en posiciones pares: """

	for i in range(len(lista)):

		if((i%2) == 0):

			salida += str(lista[i]) + " "

	salida += "</html>"
 
	return(HttpResponse(salida))

# Ejercicio: The text is given in a single line. For each word of the text count the number of its occurrences before it.

# A word is a sequence of non-whitespace characters. Two consecutive words are separated by one or more spaces.
# Punctiation marks are a part of a word, by this definition. 
def ocurrencias_palabra(request, texto):

	palabras = texto.split()
	ocurrencias = {}

	salida = "<html> "

	for p in palabras:

		if(p in ocurrencias.keys()):

			ocurrencias[p] += 1

		else:

			ocurrencias[p] = 1

	for k in ocurrencias:

		salida += k + ": " + str(ocurrencias[k]) + "<br/>"

	salida += "</html>"

	return(HttpResponse(salida))

# Ejercicio: Given a string consisting of words separated by spaces. Determine how many words it has. To solve the problem, use the method count.
# Suponemos que cada palabra está separada por solo un espacio.
def numero_palabras(request, texto):

	texto = texto.strip()
	numero_palabras = texto.count(" ") + 1

	salida = "<html> Numero palabras: " + str(numero_palabras) + "</html>"

	return(HttpResponse(salida))


# Ejercicio 1. Tarea 2. 	
# Argumentos entrada: String con una secuencia de elementos separados por ;.
# Ejemplo: sos;robar;reglar;s; ;rrrrrrrrr    
def ejercicio1(request,lista):
    
    # Crear la lista a comprobar.
    lista_strings = lista.split(";")
    cont = 0
    
    for e in lista_strings:
    
        if(len(e) >= 2 and e[0] == e[-1]):
            
            cont += 1
        
    salida = "<html> " + "Número de strings con longitud mayor o igual que 2 y con el primer caracter igual al último: " + str(cont) + "</html>"

    return(HttpResponse(salida))	

# Ejercicio 2. Tarea 2.
# Argumentos entrada: String con una secuencia de elementos separados por ;.    
# Ejemplo: 1;2;2;3;2;4;4;5;5;5;5;5;5;6   
def ejercicio2(request,lista):

    # Crear la lista a comprobar.
    lista_numeros = lista.split(";")

    # Pasar los strings a números.
    lista_numeros = [int(n) for n in lista_numeros]
    
    lista_resumida = []
    
    for i in range(len(lista_numeros)-1):
        
        if(lista_numeros[i] != lista_numeros[i+1]):
            
            lista_resumida.append(lista_numeros[i])
            
    lista_resumida.append(lista_numeros[i+1])        
        
    salida = "<html> " + "Lista de números sin adyacentes repetidos: " +  str(lista_resumida) + "<html>"
    
    return(HttpResponse(salida))

# Ejercicio 3. Tarea 2.
# Argumentos: Una cadena de caracteres.    
# Ejemplo: Spring.
def ejercicio3(request,entrada):
    
    if(len(entrada) < 2):
        
        return(HttpResponse("<html> <html>"))
        
    nueva_cadena = entrada[:2] + entrada[-2:]

    return(HttpResponse("<html> Cadena con los dos primeros y los dos últimos caracteres: " + nueva_cadena + "</html>"))

# Ejercicio 4. Tarea 2.
# Argumentos: Una cadena de caracteres.
# Ejemplo: Spring.
def ejercicio4(request,entrada):

    if(len(entrada) >= 3):

        if(entrada[-3:] == "ing"):
            
            entrada += "ly"
            
        else:
            
            entrada += "ing"

        salida = "<html> Cadena con ing o con ly añadido al final: " + entrada +  " </html>"

        return(HttpResponse(salida))            
            
    else:

        salida = "<html> Cadena sin modificar: " + entrada + " </html>"

        return(HttpResponse(salida))
        
# Ejercicio 5. Tarea 2.
# Argumentos: Un texto sin signos de puntuación, el cual se crea dentro de la propia función.
def ejercicio5(request):

    texto = """Read any text file specified on the command line
Do a simple split() on whitespace to obtain all the words in the file
Rather than read the file line by line it's easier to read
it into one giant string and split it once

Build a mimic dict that maps each word that appears in the file
to a list of all the words that immediately follow that word in the file
The list of words can be be in any order and should include
duplicates So for example the key and might have the list listing
all the words which came after and in the text
We'll say that the empty string is what comes before
the first word in the file

With the mimic dict it's fairly easy to emit random
text that mimics the original Print a word then look
up what words might come next and pick one at random as
the next work
Use the empty string as the first word to prime things
If we ever get stuck with a word that is not in the dict
go back to the empty string to keep things moving

Note the standard python module random includes a method which picks a random element
from a non-empty list

For fun feed your program to itself as input
Could work on getting it to put in linebreaks around 70
columns so the output looks better """

    palabras_texto = texto.split()
    
    mimic = {"":[palabras_texto[0]]}
    
    for i in range(len(palabras_texto)-1):
        
        if(palabras_texto[i] in mimic.keys()):
            
            # Añadir a la lista asociada a la palabra i-ésmia, la palabra
            # que le sigue.
            mimic[palabras_texto[i]].append(palabras_texto[i+1])
            
        else:
            
            # Añadir un nuevo par clave-valor al diccionario con la nueva palabra como clave y
            # cuyo valor es una lista con la palabra que aparece a continuación suyo en el texto.
            mimic[palabras_texto[i]] = [palabras_texto[i+1]]            
            
    # Generamos con el diccionario anterior un texto aleatorio de 100 palabras.
    palabra = ""
    texto_aleatorio = ""

    for i in range(10000):
        
        # Elegir una palabra de forma aleatoria para añadir al texto.
        
        if(palabra in mimic.keys()):
            
            palabras_siguientes = mimic[palabra]
            palabra = r.choice(palabras_siguientes)
        
            texto_aleatorio += " " +  palabra
        
        else:
            
            palabra = ""
        
    salida = "<html> Texto aleatorio obtenido a partir del diccionario mimic: " + texto_aleatorio + "</html>"
    
    return(HttpResponse(salida))   
        
# Realizar una función que reciba como argumento una url del períodico el país del apartado rss (últimas noticias) y
# extraer los títulos de las últimas noticias, las imágenes o ambas. Para extraer esta información utilizar expresiones regulares.
# La información extraida se debe visualizar en un archivo html del directorio templates.     
    
# Posible expresión regular para extraer los títulos. <item>\W+<title><!\[CDATA\[(.+?)\]\]><\/title> poner el testeador de regex a gms.
def extract_titles_images(request):
    
    # Obtener la página web
    pagina = requests.get("http://ep00.epimg.net/rss/tags/ultimas_noticias.xml")
    
    # Extraer todos los titulares de las noticias de la página web.
    titulares = re.findall("<item>\W*<title><!\[CDATA\[(.+?)\]\]><\/title>",pagina.text)
    
    context = {"titulares":titulares}
    
    return(render(request,"titulares.html",context))

# Función para realizar una consulta sobre la base de datos de mongo con pymongo.
# Devuelve todas las películas que pertenezcan al género indicado como argumento.
def consultaPyMongoGenero(request,genero):

	# Nos conectamos a la base de datos del contenedor mongo.
	client = MongoClient("mongo",27017)
	db = client.movies
	collection = db.pelis

	peliculas = collection.find({"genres":genero})

	# Empaquetar los resultados.
	context = {"tipoConsulta":"genero","consulta":genero,"peliculas":[]}

	for p in peliculas:

		context["peliculas"].append(p)

	return(render(request,"consultasPyMongo.html",context))

# Función para realizar una consulta sobre la base de datos de mongo con pymongo.
# Devuelve todas las películas que hayan sido dirigidas por el director recibido como argumento.
def consultaPyMongoDirector(request,director):

	# Nos conectamos a la base de datos del contenedor mongo.
	client = MongoClient("mongo",27017)
	db = client.movies
	collection = db.pelis

	peliculas = collection.find({"director":director})

	# Empaquetar los resultados.
	context = {"tipoConsulta":"director","consulta":director,"peliculas":[]}

	for p in peliculas:

		context["peliculas"].append(p)

	return(render(request,"consultasPyMongo.html",context))

# Función para realizar una consulta sobre la base de datos de mongo con pymongo.
# Devuelve todas las películas que hayan sido estrenadas en un año recibido como argumento.
def consultaPyMongoAnio(request,anio):

	# Nos conectamos a la base de datos del contenedor mongo.
	client = MongoClient("mongo",27017)
	db = client.movies
	collection = db.pelis

	peliculas = collection.find({"year":anio})

	# Empaquetar los resultados.
	context = {"tipoConsulta":"año","consulta":anio,"peliculas":[]}

	for p in peliculas:

		context["peliculas"].append(p)

	return(render(request,"consultasPyMongo.html",context))	

# Función para realizar una consulta sobre la base de datos de mongo con pymongo.
# Devuelve todas las películas en las que haya participado un actor recibido como argumento.
def consultaPyMongoActor(request,actor):

	# Nos conectamos a la base de datos del contenedor mongo.
	client = MongoClient("mongo",27017)
	db = client.movies
	collection = db.pelis

	peliculas = collection.find({"actors":actor})

	# Empaquetar los resultados.
	context = {"tipoConsulta":"actor","consulta":actor,"peliculas":[]}

	for p in peliculas:

		context["peliculas"].append(p)

	return(render(request,"consultasPyMongo.html",context))	
