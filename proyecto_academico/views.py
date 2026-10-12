from abc import ABC, abstractmethod

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido


# TUPLAS: los campos son fijos y se reutilizan al buscar y pedir datos.
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet", "carrera")
CAMPOS_MATERIA = ("nombre", "codigo", "creditos", "cupos")
BUSCABLES_ESTUDIANTE = CAMPOS_ESTUDIANTE
BUSCABLES_MATERIA = ("nombre", "codigo")


class CrudBase(ABC):

    @abstractmethod
    def leer(self):
        pass

    @abstractmethod
    def obtener(self, id_registro):
        pass

    @abstractmethod
    def buscar(self, texto):
        pass

    @abstractmethod
    def siguiente(self):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, id_registro, datos):
        pass

    @abstractmethod
    def eliminar(self, id_registro):
        pass



class EstudianteController(CrudBase):
    def __init__(self, archivo="data/estudiantes.json"):
        self.gestor = GestorJSON(archivo)
        # LISTA: conserva los objetos y permite agregarlos, recorrerlos y editarlos.
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Estudiante.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for estudiante in self.lista:
            datos.append(estudiante.a_diccionario())
        return self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        for campo in ("nombre", "apellido", "email", "carnet"):
            if datos[campo] == "":
                return f"El campo {campo} es obligatorio"
        if not es_email_valido(datos["email"]) or " " in datos["email"]:
            return "El email no tiene un formato válido"

        # CONJUNTOS: permiten comprobar carnets y emails sin repetidos.
        carnets = set()
        emails = set()
        for estudiante in self.lista:
            if estudiante.id != id_actual:
                carnets.add(estudiante.carnet.upper())
                emails.add(estudiante.email.lower())
        if datos["carnet"].upper() in carnets:
            return "Ese carnet ya está registrado"
        if datos["email"].lower() in emails:
            return "Ese email ya está registrado"
        return None

    def crear(self, datos):
        valores = {}
        for campo in CAMPOS_ESTUDIANTE:
            valores[campo] = str(datos.get(campo, "")).strip()
        valores["nombre"] = valores["nombre"].title()
        valores["apellido"] = valores["apellido"].title()
        valores["email"] = valores["email"].lower()
        valores["carnet"] = valores["carnet"].upper()
        valores["carrera"] = valores["carrera"].title()
        error = self.validar(valores)
        if error:
            return False, error
        estudiante = Estudiante(self.siguiente(), valores["nombre"],
                                valores["apellido"], valores["email"],
                                valores["carnet"], valores["carrera"])
        self.lista.append(estudiante)
        if not self.guardar():
            self.lista.pop()
            return False, "No se pudo guardar el estudiante"
        # TUPLA: devuelve el resultado y su mensaje juntos.
        return True, f"Estudiante creado con id {estudiante.id}"

    def actualizar(self, id_registro, cambios):
        estudiante = self.obtener(id_registro)
        if estudiante is None:
            return False, "No existe ese estudiante"
        if not cambios:
            return False, "No se indicó ningún cambio"
        datos = estudiante.a_diccionario()
        for campo in cambios:
            if campo not in CAMPOS_ESTUDIANTE:
                return False, f"El campo {campo} no se puede modificar"
            valor = str(cambios[campo]).strip()
            if campo in ("nombre", "apellido", "carrera"):
                valor = valor.title()
            elif campo == "email":
                valor = valor.lower()
            elif campo == "carnet":
                valor = valor.upper()
            datos[campo] = valor
        error = self.validar(datos, id_registro)
        if error:
            return False, error
        nuevo = Estudiante.desde_diccionario(datos)
        for posicion, actual in enumerate(self.lista):
            if actual.id == id_registro:
                self.lista[posicion] = nuevo
                if not self.guardar():
                    self.lista[posicion] = actual
                    return False, "No se pudo guardar la actualización"
                return True, f"Estudiante {id_registro} actualizado"
        return False, "No existe ese estudiante"

    def carreras(self):
        carreras = set()
        for estudiante in self.lista:
            if estudiante.carrera != "":
                carreras.add(estudiante.carrera)
        return sorted(carreras)

    def leer(self):
        return self.lista

    def obtener(self, id_registro):
        for objeto in self.lista:
            if objeto.id == id_registro:
                return objeto
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados
        for objeto in self.lista:
            datos = objeto.a_diccionario()
            for campo in BUSCABLES_ESTUDIANTE:
                if texto in str(datos[campo]).lower():
                    encontrados.append(objeto)
                    break
        return encontrados

    def siguiente(self):
        mayor = 0
        for objeto in self.lista:
            if objeto.id > mayor:
                mayor = objeto.id
        return mayor + 1

    def eliminar(self, id_registro):
        objeto = self.obtener(id_registro)
        if objeto is None:
            return False, "No existe ese registro"
        posicion = self.lista.index(objeto)
        self.lista.remove(objeto)
        if not self.guardar():
            self.lista.insert(posicion, objeto)
            return False, "No se pudo guardar la eliminación"
        return True, "Estudiante eliminado"


class MateriaController(CrudBase):
    def __init__(self, archivo="data/materias.json"):
        self.gestor = GestorJSON(archivo)
        # LISTA: conserva los objetos y permite agregarlos, recorrerlos y editarlos.
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Materia.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for materia in self.lista:
            datos.append(materia.a_diccionario())
        return self.gestor.guardar(datos)

    def validar(self, datos, id_actual=None):
        for campo in ("nombre", "codigo"):
            if str(datos[campo]).strip() == "":
                return f"El campo {campo} es obligatorio"
        try:
            creditos = int(str(datos["creditos"]).strip())
            cupos = int(str(datos["cupos"]).strip())
        except (TypeError, ValueError):
            return "Los créditos y cupos deben ser números enteros"
        if not (1 <= creditos <= 10):
            return "Los créditos deben estar entre 1 y 10"
        if not (0 <= cupos <= Materia.CUPOS_MAXIMOS):
            return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"

        # CONJUNTO: cada código de materia debe ser único.
        codigos = set()
        for materia in self.lista:
            if materia.id != id_actual:
                codigos.add(materia.codigo.upper())
        if datos["codigo"].upper() in codigos:
            return "Ese código ya está registrado"
        return None

    def crear(self, datos):
        valores = {}
        for campo in CAMPOS_MATERIA:
            valores[campo] = str(datos.get(campo, "")).strip()
        valores["nombre"] = valores["nombre"].title()
        valores["codigo"] = valores["codigo"].upper()
        error = self.validar(valores)
        if error:
            return False, error
        materia = Materia(self.siguiente(), valores["nombre"],
                          valores["codigo"], valores["creditos"], valores["cupos"])
        self.lista.append(materia)
        if not self.guardar():
            self.lista.pop()
            return False, "No se pudo guardar la materia"
        return True, f"Materia creada con id {materia.id}"

    def actualizar(self, id_registro, cambios):
        materia = self.obtener(id_registro)
        if materia is None:
            return False, "No existe esa materia"
        if not cambios:
            return False, "No se indicó ningún cambio"
        datos = materia.a_diccionario()
        for campo in cambios:
            if campo not in CAMPOS_MATERIA:
                return False, f"El campo {campo} no se puede modificar"
            valor = str(cambios[campo]).strip()
            if campo == "nombre":
                valor = valor.title()
            elif campo == "codigo":
                valor = valor.upper()
            datos[campo] = valor
        error = self.validar(datos, id_registro)
        if error:
            return False, error
        nuevo = Materia.desde_diccionario(datos)
        for posicion, actual in enumerate(self.lista):
            if actual.id == id_registro:
                self.lista[posicion] = nuevo
                if not self.guardar():
                    self.lista[posicion] = actual
                    return False, "No se pudo guardar la actualización"
                return True, f"Materia {id_registro} actualizada"
        return False, "No existe esa materia"

    def sin_cupo(self):
        sin_cupo = []
        for materia in self.lista:
            if not materia.hay_cupo():
                sin_cupo.append(materia)
        return sin_cupo

    def leer(self):
        return self.lista

    def obtener(self, id_registro):
        for objeto in self.lista:
            if objeto.id == id_registro:
                return objeto
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontrados = []
        if texto == "":
            return encontrados
        for objeto in self.lista:
            datos = objeto.a_diccionario()
            for campo in BUSCABLES_MATERIA:
                if texto in str(datos[campo]).lower():
                    encontrados.append(objeto)
                    break
        return encontrados

    def siguiente(self):
        mayor = 0
        for objeto in self.lista:
            if objeto.id > mayor:
                mayor = objeto.id
        return mayor + 1

    def eliminar(self, id_registro):
        objeto = self.obtener(id_registro)
        if objeto is None:
            return False, "No existe ese registro"
        posicion = self.lista.index(objeto)
        self.lista.remove(objeto)
        if not self.guardar():
            self.lista.insert(posicion, objeto)
            return False, "No se pudo guardar la eliminación"
        return True, "Registro de materia eliminado"


class MatriculaController(CrudBase):
    def __init__(self, estudiantes, materias, archivo="data/matriculas.json"):
        self.estudiantes = estudiantes
        self.materias = materias
        self.gestor = GestorJSON(archivo)
        # LISTA: conserva los objetos y permite agregarlos, recorrerlos y editarlos.
        self.lista = []
        for datos in self.gestor.leer():
            self.lista.append(Matricula.desde_diccionario(datos))

    def guardar(self):
        datos = []
        for matricula in self.lista:
            datos.append(matricula.a_diccionario())
        return self.gestor.guardar(datos)

    def leer(self):
        return self.lista

    def obtener(self, id_registro):
        for matricula in self.lista:
            if matricula.id == id_registro:
                return matricula
        return None

    def buscar(self, texto):
        texto = texto.strip().lower()
        encontradas = []
        if texto == "":
            return encontradas
        for matricula in self.lista:
            if texto in matricula.periodo.lower():
                encontradas.append(matricula)
        return encontradas

    def siguiente(self):
        mayor = 0
        for matricula in self.lista:
            if matricula.id > mayor:
                mayor = matricula.id
        return mayor + 1

    def validar(self, datos):
        try:
            estudiante_id = int(str(datos.get("estudiante_id", "")).strip())
            materia_id = int(str(datos.get("materia_id", "")).strip())
        except (TypeError, ValueError):
            return "Los IDs del estudiante y de la materia deben ser enteros"
        periodo = str(datos.get("periodo", "")).strip()
        if periodo == "":
            return "El periodo es obligatorio"

        # CONJUNTOS: permiten comprobar si los IDs existen.
        ids_estudiantes = set()
        for estudiante in self.estudiantes.leer():
            ids_estudiantes.add(estudiante.id)
        ids_materias = set()
        for materia in self.materias.leer():
            ids_materias.add(materia.id)
        if estudiante_id not in ids_estudiantes:
            return "No existe ese estudiante"
        if materia_id not in ids_materias:
            return "No existe esa materia"
        materia = self.materias.obtener(materia_id)
        if not materia.hay_cupo():
            return "La materia no tiene cupos disponibles"
        for matricula in self.lista:
            if (matricula.estudiante_id == estudiante_id
                    and matricula.materia_id == materia_id
                    and matricula.periodo.lower() == periodo.lower()):
                return "El estudiante ya está matriculado en esa materia y periodo"
        if not Materia.es_nota_valida(datos.get("nota", 0)):
            return "La nota debe ser un número entre 0 y 20"
        return None

    def crear(self, datos):
        error = self.validar(datos)
        if error:
            return False, error
        matricula = Matricula(self.siguiente(),
                              int(str(datos["estudiante_id"]).strip()),
                              int(str(datos["materia_id"]).strip()),
                              str(datos["periodo"]).strip(),
                              float(str(datos.get("nota", 0)).strip()))
        materia = self.materias.obtener(matricula.materia_id)
        cupos_anteriores = materia.cupos
        materia.ocupar_cupo()
        if not self.materias.guardar():
            materia.cupos = cupos_anteriores
            return False, "No se pudo guardar el cambio de cupos"
        self.lista.append(matricula)
        if not self.guardar():
            self.lista.pop()
            materia.cupos = cupos_anteriores
            if not self.materias.guardar():
                return False, "Falló la matrícula y no se pudo restaurar el archivo de cupos"
            return False, "No se pudo guardar la matrícula"
        return True, f"Matrícula {matricula.id} registrada"

    def actualizar(self, id_registro, datos):
        if not datos or "nota" not in datos or len(datos) != 1:
            return False, "Solo se puede actualizar la nota de la matrícula"
        return self.registrar_nota(id_registro, datos["nota"])

    def registrar_nota(self, id_registro, nota):
        matricula = self.obtener(id_registro)
        if matricula is None:
            return False, "No existe esa matrícula"
        if not Materia.es_nota_valida(nota):
            return False, "La nota debe ser un número entre 0 y 20"
        anterior = matricula.nota
        matricula.nota = float(str(nota).strip())
        if not self.guardar():
            matricula.nota = anterior
            return False, "No se pudo guardar la nota"
        return True, f"Nota registrada: {matricula.nota:g} · {matricula.estado()}"

    def eliminar(self, id_registro):
        matricula = self.obtener(id_registro)
        if matricula is None:
            return False, "No existe esa matrícula"
        materia = self.materias.obtener(matricula.materia_id)
        if materia is not None:
            if materia.cupos >= Materia.CUPOS_MAXIMOS:
                return False, "No se puede devolver el cupo: la materia ya tiene 30 cupos"
            cupos_anteriores = materia.cupos
            materia.liberar_cupo()
            if not self.materias.guardar():
                materia.cupos = cupos_anteriores
                return False, "No se pudo guardar la devolución del cupo"
        posicion = self.lista.index(matricula)
        self.lista.remove(matricula)
        if not self.guardar():
            self.lista.insert(posicion, matricula)
            if materia is not None:
                materia.cupos = cupos_anteriores
                if not self.materias.guardar():
                    return False, "Falló el retiro y no se pudo restaurar el archivo de cupos"
            return False, "No se pudo guardar el retiro"
        if materia is None:
            return True, "Matrícula retirada; la materia había sido eliminada"
        return True, "Matrícula retirada y cupo devuelto"

    def certificado(self, id_registro):
        matricula = self.obtener(id_registro)
        if matricula is None:
            return None

        # DICCIONARIOS ÍNDICE: relacionan los objetos por su ID.
        indice_estudiantes = {}
        for estudiante in self.estudiantes.leer():
            indice_estudiantes[estudiante.id] = estudiante
        indice_materias = {}
        for materia in self.materias.leer():
            indice_materias[materia.id] = materia
        estudiante = indice_estudiantes.get(matricula.estudiante_id)
        materia = indice_materias.get(matricula.materia_id)

        texto = f"CERTIFICADO #{matricula.id}   periodo: {matricula.periodo}\n"
        if estudiante is None:
            texto += "Estudiante: eliminado\n"
        else:
            texto += f"Estudiante: {estudiante.nombre_completo()}   ({estudiante.carnet})\n"
        if materia is None:
            texto += "Materia   : eliminada\n"
        else:
            texto += (f"Materia   : {materia.nombre}   ({materia.codigo}) · "
                      f"{materia.creditos} créditos\n")
        texto += "-" * 42 + "\n"
        texto += f"Nota      : {matricula.nota:g}\n"
        texto += f"Estado    : {matricula.estado()}"
        return texto

    def por_estudiante(self):
        # DICCIONARIO DE LISTAS: reúne las matrículas de cada estudiante.
        agrupadas = {}
        for matricula in self.lista:
            agrupadas.setdefault(matricula.estudiante_id, []).append(matricula)
        return agrupadas

    def promedio(self, id_estudiante):
        if self.estudiantes.obtener(id_estudiante) is None:
            return None
        total = 0
        cantidad = 0
        for matricula in self.lista:
            if matricula.estudiante_id == id_estudiante:
                total = total + matricula.nota
                cantidad = cantidad + 1
        if cantidad == 0:
            return 0
        return round(total / cantidad, 2)

    def cantidad_aprobadas(self):
        cantidad = 0
        for matricula in self.lista:
            if matricula.esta_aprobada():
                cantidad = cantidad + 1
        return cantidad


estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)


def crear_estudiante(datos):
    return estudiantes.crear(datos)


def obtener_estudiantes():
    return estudiantes.leer()


def obtener_estudiante(id_registro):
    return estudiantes.obtener(id_registro)


def buscar_estudiantes(termino):
    return estudiantes.buscar(termino)


def actualizar_estudiante(id_registro, cambios):
    return estudiantes.actualizar(id_registro, cambios)


def eliminar_estudiante(id_registro):
    return estudiantes.eliminar(id_registro)


def crear_materia(datos):
    return materias.crear(datos)


def obtener_materias():
    return materias.leer()


def obtener_materia(id_registro):
    return materias.obtener(id_registro)


def buscar_materias(termino):
    return materias.buscar(termino)


def actualizar_materia(id_registro, cambios):
    return materias.actualizar(id_registro, cambios)


def eliminar_materia(id_registro):
    return materias.eliminar(id_registro)


def materias_sin_cupo():
    return materias.sin_cupo()


def crear_matricula(datos):
    return matriculas.crear(datos)


def obtener_matriculas():
    return matriculas.leer()


def obtener_matricula(id_registro):
    return matriculas.obtener(id_registro)


def registrar_nota(id_registro, nota):
    return matriculas.registrar_nota(id_registro, nota)


def retirar_matricula(id_registro):
    return matriculas.eliminar(id_registro)


def certificado(id_registro):
    return matriculas.certificado(id_registro)


def matriculas_por_estudiante():
    return matriculas.por_estudiante()


def promedio_de_estudiante(id_estudiante):
    return matriculas.promedio(id_estudiante)
