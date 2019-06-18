from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .viewsets import PelisViewSet
from . import views

router = routers.DefaultRouter()
router.register('pelis', PelisViewSet, 'peli')

urlpatterns = [

	path('genero/<str:genero>', views.consultaGenero),
	path('director/<str:director>', views.consultaDirector),
	path('anio/<int:anio>', views.consultaAnio),
	path('consulta', views.consulta,name="consulta"),
	path('resultadoConsulta', views.resultadoConsulta),
	path('id/<id>',views.info_de,name = 'info_de'),
	path('editar/<id>',views.editar_pelicula,name='editar'),
	path('crear/',views.crear_pelicula,name='crear'),
	path('eliminar/<id>',views.eliminar_pelicula,name='eliminar'),
	path('peliculaEliminada',views.pelicula_eliminada,name='pelicula_eliminada'),
	path('home',views.home,name="home"),
	path('likeDislike',views.actualizar_likes,name="likeDislike"),
	path('api_pelis',views.api_pelis),
	path('api_peli/<id>', views.api_peli),
	url('api',include(router.urls))
]

