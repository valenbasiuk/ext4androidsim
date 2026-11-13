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

    def calcular_metricas(self):
        # Desafío 1: reporte de métricas del almacenamiento
        print("\n--- Métricas del disco ---")
        # Recorrer el disco: None = libre, cualquier otro valor = ocupado
        ocupados = 0
        libres = 0
        for b in self.bloques:
            if b is None:
                libres += 1
            else:
                ocupados += 1

        print(f"Total de bloques: {self.total_bloques}")
        print(f"Bloques ocupados: {ocupados}")
        print(f"Bloques libres: {libres}")

        # Ocupación (%) = (Bloques Ocupados / Total de Bloques) x 100
        if self.total_bloques > 0:
            ocupacion = (ocupados / self.total_bloques) * 100
        else:
            ocupacion = 0  # Disco sin bloques: se evita dividir por cero
        print(f"Porcentaje de ocupación: {ocupacion:.2f}%")

    def calcular_fragmentacion_externa(self):
        max_hueco = 0
        hueco_actual = 0
        total_libres = 0

        # Recorrer los bloques para encontrar el mayor hueco contiguo y el total de libres
        for b in self.bloques:
            if b is None:
                hueco_actual += 1
                total_libres += 1
                # Actualizamos el hueco máximo si el actual lo supera
                if hueco_actual > max_hueco:
                    max_hueco = hueco_actual
            else:
                # Si encontramos un bloque ocupado, se corta la secuencia (hueco) actual
                hueco_actual = 0

        # Aplicar la fórmula de fragmentación externa
        if total_libres == 0:
            fragmentacion = 0.0  # Si no hay espacio libre, la fragmentación es 0%
        else:
            fragmentacion = (1 - (max_hueco / total_libres)) * 100
        
        # Imprimir los resultados
        print("\n --- Análisis de Fragmentación --- ")
        print(f"Mayor hueco contiguo libre: {max_hueco}")
        print(f"Total de bloques libres: {total_libres}")
        print(f"Fragmentación Externa: {fragmentacion:.2f}%")
        
        return fragmentacion


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

def ejecutar_caso_prueba():
    print("\n=======================================")
    print("   EJECUTANDO CASO DE PRUEBA PRÁCTICO")
    print("=======================================")
    
    disco = SimuladorDisco(64)
    
    print("\nPaso 1: Crear docA.txt, docB.txt y docC.txt (4 bloques c/u)")
    disco.crear_archivo("docA.txt", 4)
    disco.crear_archivo("docB.txt", 4)
    disco.crear_archivo("docC.txt", 4)
    
    print("\nPaso 2: Eliminar docB.txt")
    disco.eliminar_archivo("docB.txt")
    
    print("\nPaso 3: Crear docD.txt (6 bloques)")
    disco.crear_archivo("docD.txt", 6)
    
    disco.mostrar_mapa()
    mostrar_tabla_inodos(disco)
    mostrar_metricas(disco)

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
        print("6. Ejecutar Caso de Prueba Automático")
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
        elif opcion == "6":
            ejecutar_caso_prueba()

        else:
            print("Opción inválida. Ingrese un número del 1 al 5.")


if __name__ == "__main__":
    menu()
