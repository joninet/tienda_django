from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria,on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField(null=True)
    precio = models.DecimalField(max_digits=9,decimal_places=2)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos',blank=True)
    
    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    usuario = models.OneToOneField(User,on_delete=models.RESTRICT)
    dni = models.CharField(max_length=8)
    sexo = models.CharField(max_length=1, default="M")
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True)
    direccion = models.TextField()

    def __str__(self):
        return self.dni
    
class Pedido(models.Model):
    estado_choices = (
        ('0', 'Pendiente'),
        ('1', 'Pagado')
    )
    cliente= models.OnetoManyField(Cliente,on_delete=RESTRICT)
    fecha_registro = models.DateTimeField(auto)
    nro_pedido =
    monto_total =
    estado =