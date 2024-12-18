from django.shortcuts import render, get_object_or_404, redirect

from .models import Categoria, Producto, Cliente
from .carrito import Cart

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import ClienteForm
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

def productosPorNombre(request):
    nombre = request.POST['nombre']

    listaProductos = Producto.objects.filter(nombre__contains=nombre)
    listaCategorias = Categoria.objects.all()

    context = {
        'productos':listaProductos,
        'categorias':listaCategorias
    }
    return render(request, 'index.html', context)

def detalleProducto(request, producto_id):
    #objProducto = Producto.objects.get(pk=producto_id)

    objProducto = get_object_or_404(Producto, pk=producto_id)

    context = {
        'producto' : objProducto
    }
    
    return render(request, 'producto.html', context)

def carrito(request):
    return render(request, 'carrito.html')

def agregarCarrito(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
    else:
        cantidad = 1
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.add(objProducto, cantidad)

    if request.method == 'GET':
        return redirect('/')

    return render(request, 'carrito.html')

def eliminarProductoCarrito(request, producto_id):
    objProducto = Producto.objects.get(pk=producto_id)
    carritoProducto = Cart(request)
    carritoProducto.delete(objProducto)

    return render(request, 'carrito.html')

def limpiarCarrito (request):
    carritoProducto = Cart(request)
    carritoProducto.clear()
    return render(request,'carrito.html')

def crearUsuario(request):
    if request.method == 'POST':
        dataUsuario = request.POST['nuevoUsuario']
        dataPassword = request.POST['nuevoPassword']
        nuevoUsuario = User.objects.create_user(username=dataUsuario, password=dataPassword)
        if nuevoUsuario is not None:
            login(request,nuevoUsuario)
            return redirect('/cuenta')

    return render(request, 'login.html')

def loginUsuario(request):
    context = {}
    if request.method == 'POST':
        dataUsuario = request.POST['usuario']
        dataPassword = request.POST['password']

        usuarioAuth = authenticate(request, username=dataUsuario,password=dataPassword)

        if usuarioAuth is not None:
            login(request, usuarioAuth)
            return redirect('/cuenta')
        else:
            context = {
                'mensajeError':'Datos Incorrectos'
            }

    return render(request, 'login.html', context)

def cuentaUsuario(request):
    try:
        clienteEditar = Cliente.objects.get(usuario = request.user)

        dataCliente = {
            'nombres':request.user.first_name,
            'apellidos':request.user.last_name,
            'email':request.user.email,
            'direccion': clienteEditar.direccion,
            'telefono': clienteEditar.telefono,
            'dni': clienteEditar.dni,
            'sexo': clienteEditar.sexo,
            'fecha_nacimiento': clienteEditar.fecha_nacimiento
        }
    except:
        dataCliente = {
            'nombres':request.user.first_name,
            'apellidos':request.user.first_name,
            'email':request.user.email
            }

    frmCliente = ClienteForm(dataCliente)

    context = {
        'frmCliente' : frmCliente
    }

    return render(request,'cuenta.html', context)

def actualizarCliente(request):
    mensaje = ""

    if request.method == 'POST':
        frmCliente = ClienteForm(request.POST)
        if frmCliente.is_valid():
            dataCliente = frmCliente.cleaned_data

            # Actualizar usuario
            actUsuario = User.objects.get(pk=request.user.id)
            actUsuario.first_name = dataCliente["nombres"]
            actUsuario.last_name = dataCliente["apellidos"]
            actUsuario.email = dataCliente["email"]
            actUsuario.save()

            # Buscar o crear cliente
            try:
                # Intentar obtener el cliente existente
                nuevoCliente = Cliente.objects.get(usuario=actUsuario)
                
                # Actualizar los campos existentes
                nuevoCliente.dni = dataCliente["dni"]
                nuevoCliente.direccion = dataCliente["direccion"]
                nuevoCliente.telefono = dataCliente["telefono"]  
                nuevoCliente.sexo = dataCliente["sexo"]
                nuevoCliente.fecha_nacimiento = dataCliente["fecha_nacimiento"]
            except Cliente.DoesNotExist:
                # Si no existe, crear un nuevo cliente
                nuevoCliente = Cliente(
                    usuario=actUsuario,
                    dni=dataCliente["dni"],
                    direccion=dataCliente["direccion"],
                    telefono=dataCliente["telefono"],
                    sexo=dataCliente["sexo"],
                    fecha_nacimiento=dataCliente["fecha_nacimiento"]
                )
            
            nuevoCliente.save()
            mensaje = "Datos Actualizados"

    context = {
        'mensaje': mensaje,
        'frmCliente': frmCliente
    }
    return render(request, 'cuenta.html', context)

