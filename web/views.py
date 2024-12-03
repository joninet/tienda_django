from django.shortcuts import render

from .models import Categoria, Producto
# Create your views here.

"""vistas para el catalogo de productos"""
def index(request):
    listaCategorias = Categoria.objects.all()
    listaProductos = Producto.objects.all()
    context = {
        'productos':listaProductos,
        'categorias':listaCategorias
    }

    return render(request,'index.html', context)

def productosPorCategoria(request, categoria_id):
    objCategoria = Categoria.objects.get(pk=categoria_id)
    listaProductos = objCategoria.producto_set.all()
    listaCategorias = Categoria.objects.all()
    context = {
        'productos':listaProductos,
        'categorias':listaCategorias}
    
    return render(request,'index.html', context)
