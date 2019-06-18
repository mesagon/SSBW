from django.urls import path

from . import views

urlpatterns = [
	path('hola_mundo/<str:usuario>', views.hola_mundo),
	path('posiciones_pares', views.posiciones_pares),
	path('ocurrencias_palabra/<str:texto>', views.ocurrencias_palabra),
	path('numero_palabras/<str:texto>', views.numero_palabras),
    	path('ejercicio1/<str:lista>', views.ejercicio1),
    	path('ejercicio2/<str:lista>', views.ejercicio2),
    	path('ejercicio3/<str:entrada>', views.ejercicio3),
    	path('ejercicio4/<str:entrada>', views.ejercicio4),
    	path('ejercicio5', views.ejercicio5),
    	path('extract_titles_images',views.extract_titles_images),
    	path('peliculas/genero/<str:genero>', views.consultaPyMongoGenero),
    	path('peliculas/director/<str:director>', views.consultaPyMongoDirector),
    	path('peliculas/anio/<int:anio>',views.consultaPyMongoAnio),
	path('peliculas/actor/<str:actor>',views.consultaPyMongoActor)
]

