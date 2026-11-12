class Inodo:
    def __init__(self, nombre, tam_bloques):
        self.nombre = nombre
        self.tam_bloques = tam_bloques
        self.bloques_asignados = []  # Lista de índices de bloques en disco

class SimuladorDisco:
    def __init__(self, total_bloques=64):
        self.total_bloques = total_bloques
        # None indica bloque libre, de lo contrario guarda el nombre del archivo
        self.bloques = [None] * total_bloques
        self.tabla_inodos = {}

    def crear_archivo(self, nombre, tam_bloques):
        # 1. Validar nombre duplicado
        if nombre in self.tabla_inodos:
            print(f"Error: El archivo '{nombre}' ya existe.")
            return False

        # 2. Buscar bloques libres
        bloques_libres = [i for i, b in enumerate(self.bloques) if b is None]
        if len(bloques_libres) < tam_bloques:
            print("Error: Espacio en disco insuficiente / Bloques agotados.")
            return False

        # 3. Asignación indexada (toma los primeros libres disponibles)
        nuevo_inodo = Inodo(nombre, tam_bloques)
        for i in range(tam_bloques):
            idx = bloques_libres[i]
            self.bloques[idx] = nombre
            nuevo_inodo.bloques_asignados.append(idx)

        self.tabla_inodos[nombre] = nuevo_inodo
        print(f"Archivo '{nombre}' creado con éxito. Bloques asignados: {nuevo_inodo.bloques_asignados}")
        return True

    def eliminar_archivo(self, nombre):
        if nombre not in self.tabla_inodos:
            print(f"Error: Archivo '{nombre}' no encontrado.")
            return False

        inodo = self.tabla_inodos[nombre]
        for idx in inodo.bloques_asignados:
            self.bloques[idx] = None

        del self.tabla_inodos[nombre]
        print(f"Archivo '{nombre}' eliminado correctamente.")
        return True

    def mostrar_mapa(self):
        mapa = "".join(["[O]" if b else "[L]" for b in self.bloques])
        print("\nMapa del Disco (Primeros bloques):", mapa)

# =====================================================================
# DESAFÍO 3: Menú interactivo de operaciones
# =====================================================================

def mostrar_tabla_inodos(disco):
    """Muestra la tabla de inodos: cada archivo con su tamaño y sus punteros a bloques."""
    print("\nTabla de Inodos:")
    if not disco.tabla_inodos:
        print("  (no hay archivos en el disco)")
        return
    print(f"  {'Archivo':<15}{'Tamaño (bloques)':<18}Bloques asignados")
    for inodo in disco.tabla_inodos.values():
        print(f"  {inodo.nombre:<15}{inodo.tam_bloques:<18}{inodo.bloques_asignados}")


def mostrar_metricas(disco):
    """Muestra las métricas de los Desafíos 1 y 2 (si ya están programadas)."""
    if hasattr(disco, "calcular_metricas"):
        disco.calcular_metricas()
    else:
        print("\nMétricas: pendiente (Desafío 1).")
    if hasattr(disco, "calcular_fragmentacion_externa"):
        disco.calcular_fragmentacion_externa()
    else:
        print("Fragmentación externa: pendiente (Desafío 2).")


def pedir_tamano():
    """Pide el tamaño en bloques y valida que sea un entero mayor a 0."""
    valor = input("Tamaño en bloques: ").strip()
    if not valor.isdigit() or int(valor) == 0:
        print("Error: el tamaño debe ser un número entero mayor a 0.")
        return None
    return int(valor)


def menu():
    disco = SimuladorDisco(64)

    while True:
        print("\n=======================================")
        print("   SIMULADOR DE SISTEMA DE ARCHIVOS")
        print("=======================================")
        print("1. Crear archivo")
        print("2. Eliminar archivo")
        print("3. Ver mapa de bloques")
        print("4. Ver tabla de Inodos y métricas")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del archivo: ").strip()
            if not nombre:
                print("Error: el nombre no puede estar vacío.")
                continue
            tam = pedir_tamano()
            if tam is not None:
                disco.crear_archivo(nombre, tam)
                disco.mostrar_mapa()

        elif opcion == "2":
            nombre = input("Nombre del archivo a eliminar: ").strip()
            disco.eliminar_archivo(nombre)
            disco.mostrar_mapa()

        elif opcion == "3":
            disco.mostrar_mapa()

        elif opcion == "4":
            mostrar_tabla_inodos(disco)
            mostrar_metricas(disco)

        elif opcion == "5":
            print("Saliendo del simulador...")
            break

        else:
            print("Opción inválida. Ingrese un número del 1 al 5.")


if __name__ == "__main__":
    menu()
