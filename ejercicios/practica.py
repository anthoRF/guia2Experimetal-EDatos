from models import Persona, Cliente, Producto, Venta
from views import (
    ClienteController, ProductoController, VentaController, clientes_por_ciudad
)


# Ejercicio 1: quitar duplicados conservando el orden.
ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
vistas = set()
unicas = []
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)
print("Ejercicio 1:", unicas)

# Ejercicio 2: contar con un diccionario.
conteo = {}
for ciudad in ciudades:
    if ciudad not in conteo:
        conteo[ciudad] = 0
    conteo[ciudad] = conteo[ciudad] + 1
mas_repetida = ""
mayor = 0
for ciudad in conteo:
    if conteo[ciudad] > mayor:
        mayor = conteo[ciudad]
        mas_repetida = ciudad
print("Ejercicio 2:", conteo, "Más repetida:", mas_repetida)

# Ejercicio 3: intersección, diferencia y unión de conjuntos.
inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
inscritos_ingles = {"Luis", "Marco", "Ruth"}
ambas = inscritos_matematica & inscritos_ingles
solo_mate = inscritos_matematica - inscritos_ingles
total = len(inscritos_matematica | inscritos_ingles)
print("Ejercicio 3:", sorted(ambas), sorted(solo_mate), total)

# Ejercicio 4: crear un diccionario índice por ID.
clientes_datos = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
indice = {}
for cliente in clientes_datos:
    indice[cliente["id"]] = cliente
print("Ejercicio 4:", indice[2]["nombre"])

# Ejercicio 5: desempaquetar tuplas y calcular con un recorrido.
ventas_datos = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]
total = 0
mejor_mes, mejor_monto = ventas_datos[0]
for mes, monto in ventas_datos:
    total = total + monto
    if monto > mejor_monto:
        mejor_mes = mes
        mejor_monto = monto
print("Ejercicio 5:", "Total:", total, "Mejor mes:", mejor_mes, mejor_monto)

# Ejercicio 6: agrupar los clientes por ciudad.
clientes = ClienteController("data/clientes.json")
print("Ejercicio 6:", clientes_por_ciudad(clientes))

# Ejercicio 7: clasificar métodos y justificar su tipo.
print("Ejercicio 7:")
print("a) calcular_total: de instancia; usa cantidad y precio de esa venta.")
print("b) desde_diccionario: de clase; crea un objeto de la clase que llamó.")
print("c) es_precio_valido: estático; recibe un valor y aplica una regla.")
print("d) stock_bajo: de instancia; consulta el stock de ese producto.")
print("e) con_iva: estático; calcula el IVA de un monto recibido.")

# Ejercicio 8: reutilizar Persona para construir Proveedor.
class Proveedor(Persona):
    def __init__(self, id_registro, nombre, apellido, email, ruc="", empresa=""):
        super().__init__(id_registro, nombre, apellido, email)
        self.ruc = ruc
        self.empresa = empresa

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["ruc"] = self.ruc
        datos["empresa"] = self.empresa
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · {self.empresa} · RUC {self.ruc}"


proveedor = Proveedor.desde_diccionario({
    "id": 1, "nombre": "Luis", "apellido": "Mora", "email": "luis@x.com",
    "ruc": "0912345678001", "empresa": "Importadora Sur"
})
print("Ejercicio 8:", proveedor)

# Ejercicio 9: cada objeto sabe describirse mediante etiqueta().
def describir(objeto):
    return objeto.etiqueta()


cliente = Cliente(1, "Ana", "Pérez", "ana@x.com", "0987654321", "Guayaquil")
producto = Producto(1, "Teclado", 25.5, 30)
venta = Venta(1, 1, 1, 2, 25.5)
print("Ejercicio 9:")
for objeto in [cliente, producto, venta, proveedor]:
    print(describir(objeto))

# Ejercicio 10: descuento mayorista desde 12 unidades.
print("Ejercicio 10:")
print("Precio por unidad al comprar 11:", Producto.precio_mayorista(25.5, 11))
print("Precio por unidad al comprar 12:", Producto.precio_mayorista(25.5, 12))
productos = ProductoController("data/productos.json")
ventas = VentaController(clientes, productos, "data/ventas.json")
print("El comprobante aplica el descuento al registrar una venta de 12 o más unidades.")
