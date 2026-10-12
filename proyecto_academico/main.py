from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    estudiantes, materias, matriculas, CAMPOS_ESTUDIANTE, CAMPOS_MATERIA
)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    """Devuelve un entero o None si el usuario escribió otra cosa."""
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    # Los controladores devuelven la TUPLA (exito, mensaje)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    """Sirve para clientes, productos y ventas: cada modelo sabe mostrarse."""
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    # Recorre el DICCIONARIO del objeto: clave y valor a la vez
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")



def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")
    exito, mensaje = estudiantes.crear(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer())
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Término de búsqueda: ")
    mostrar_lista(estudiantes.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    objeto = estudiantes.obtener(pedir_entero("Id: "))
    if objeto is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(objeto)
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_registro = pedir_entero("Id: ")
    objeto = estudiantes.obtener(id_registro)
    if objeto is None:
        imprimir_error("No encontrado")
        pausa()
        return
    imprimir_info(f"Editando: {objeto.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")
    datos = objeto.a_diccionario()
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        nuevo = input(f"{campo.capitalize()} [{datos[campo]}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo
    exito, mensaje = estudiantes.actualizar(id_registro, cambios)
    mostrar_resultado(exito, mensaje)
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_registro = pedir_entero("Id: ")
    objeto = estudiantes.obtener(id_registro)
    if objeto is None:
        imprimir_error("No encontrado")
        pausa()
        return
    imprimir_info(f"Se eliminará: {objeto.etiqueta()}")
    if confirmar("¿Confirma?"):
        exito, mensaje = estudiantes.eliminar(id_registro)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {}
    for campo in CAMPOS_MATERIA:
        datos[campo] = input(f"{campo.capitalize()}: ")
    exito, mensaje = materias.crear(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer())
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Término de búsqueda: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    objeto = materias.obtener(pedir_entero("Id: "))
    if objeto is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(objeto)
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_registro = pedir_entero("Id: ")
    objeto = materias.obtener(id_registro)
    if objeto is None:
        imprimir_error("No encontrado")
        pausa()
        return
    imprimir_info(f"Editando: {objeto.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")
    datos = objeto.a_diccionario()
    cambios = {}
    for campo in CAMPOS_MATERIA:
        nuevo = input(f"{campo.capitalize()} [{datos[campo]}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo
    exito, mensaje = materias.actualizar(id_registro, cambios)
    mostrar_resultado(exito, mensaje)
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_registro = pedir_entero("Id: ")
    objeto = materias.obtener(id_registro)
    if objeto is None:
        imprimir_error("No encontrado")
        pausa()
        return
    imprimir_info(f"Se eliminará: {objeto.etiqueta()}")
    if confirmar("¿Confirma?"):
        exito, mensaje = materias.eliminar(id_registro)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def matricular():
    imprimir_titulo("MATRICULAR ESTUDIANTE")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())
    datos = {
        "estudiante_id": pedir_entero("Id del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo: "),
    }
    exito, mensaje = matriculas.crear(datos)
    mostrar_resultado(exito, mensaje)
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRÍCULAS")
    mostrar_lista(matriculas.leer())
    pausa()


def registrar_nota():
    imprimir_titulo("REGISTRAR NOTA")
    id_registro = pedir_entero("Id de la matrícula: ")
    nota = input("Nota entre 0 y 20: ")
    exito, mensaje = matriculas.registrar_nota(id_registro, nota)
    mostrar_resultado(exito, mensaje)
    pausa()


def ver_certificado():
    imprimir_titulo("CERTIFICADO")
    texto = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if texto is None:
        imprimir_error("No existe esa matrícula")
    else:
        print(texto)
    pausa()


def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")
    id_registro = pedir_entero("Id de la matrícula: ")
    objeto = matriculas.obtener(id_registro)
    if objeto is None:
        imprimir_error("No existe esa matrícula")
        pausa()
        return
    imprimir_info(objeto.etiqueta())
    if confirmar("Se devolverá el cupo. ¿Confirma?"):
        exito, mensaje = matriculas.eliminar(id_registro)
        mostrar_resultado(exito, mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN ACADÉMICO")
    print(f"  Estudiantes: {len(estudiantes.leer())}")
    carreras = estudiantes.carreras()
    if carreras:
        print("  Carreras: " + ", ".join(carreras))
    else:
        print("  Carreras: ninguna")
    imprimir_info("Materias sin cupo:")
    mostrar_lista(materias.sin_cupo(), "Ninguna materia sin cupo.")
    print(f"  Matrículas aprobadas: {matriculas.cantidad_aprobadas()}")
    pausa()


# DICCIONARIO: cada tecla se relaciona con el texto y la función del menú.
MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Matricular", matricular),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota),
    "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()
        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue
        texto, funcion = opciones[tecla]
        if funcion is None:
            break
        try:
            funcion()
        except (KeyError, TypeError, ValueError, OSError) as error:
            imprimir_error(f"No se pudo completar la operación: {error}")
            pausa()


def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")
        tecla = input("Opción: ").strip()
        if tecla == "1":
            ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3":
            ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)
        elif tecla == "4":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego!")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
