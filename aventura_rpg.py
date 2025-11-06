import random
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

class Personaje:
    def __init__(self, nombre, vidas, ataque):
        self.nombre = nombre
        self.vidas = vidas
        self.ataque = ataque
        self.esta_defendiendo = False

    def atacar(self, enemigo):
        enemigo.vidas -= self.ataque
        print(Fore.GREEN + f"¡Atacas al {enemigo.nombre} con todas tus fuerzas!")
        print(Fore.GREEN + f"Le infliges {self.ataque} de daño.")

    def defender(self):
        self.esta_defendiendo = True
        print(Fore.BLUE + "Te preparas para el impacto, subiendo tu guardia.")

# Diccionario de monstruos
catalogo_monstruos = {
    "Goblin": {"vidas": 60, "ataque": 12},
    "Ogro": {"vidas": 60, "ataque": 12},
    "Orco": {"vidas": 60, "ataque": 12},
    "Slime": {"vidas": 60, "ataque": 12}
}

# Función principal del juego
def main():
    print(Fore.YELLOW + "¡Bienvenido a las cavernas de la actividad 3!")
    nombre_heroe = input(Fore.YELLOW + "Introduce el nombre de tu héroe: ")

    # Crear instancia del jugador
    jugador = Personaje(nombre_heroe, 100, 15)

    print("------------------------------------------------")
    print(f"Hola, {jugador.nombre}. Tus estadísticas son:")
    print(f"  Vida: {jugador.vidas}")
    print(f"  Ataque: {jugador.ataque}")
    print(f"  Defensa: {jugador.ataque}")
    print("------------------------------------------------")

    # Selección de camino
    print("Llegas a una bifurcación en el camino.")
    print("Un camino lleva al bosque tranquilo, el otro a una cueva oscura.")
    print(" ")
    print(Fore.YELLOW + "1. Ir por el bosque (Ruta Segura).")
    print(Fore.YELLOW + "2. Entrar a la cueva (Ruta Peligrosa).")
    decision_camino = int(input())

    if decision_camino == 1:
        print("Decides tomar el camino del bosque.")
        print("Es un paseo agradable y llegas al pueblo sin incidentes.")
    elif decision_camino == 2:
        print("Con valentía, entras en la cueva oscura...")

        # Seleccionar monstruo al azar
        nombre_monstruo = random.choice(list(catalogo_monstruos.keys()))
        stats = catalogo_monstruos[nombre_monstruo]
        monstruo = Personaje(nombre_monstruo, stats["vidas"], stats["ataque"])

        print(f"¡Un {monstruo.nombre} salvaje aparece!")
        print(Fore.YELLOW + "¡COMIENZA EL COMBATE!")

        # Bucle de combate
        while jugador.vidas > 0 and monstruo.vidas > 0:
            print("--- NUEVO TURNO ---")
            print(f"Vida de {jugador.nombre}: {jugador.vidas}")
            print(f"Vida del {monstruo.nombre}: {monstruo.vidas}")
            print(" ")
            print(Fore.YELLOW + "¿Qué harás?")
            print(Fore.YELLOW + f"1. Atacar ({jugador.ataque} de daño)")
            print(Fore.YELLOW + "2. Defenderse (reduce el próximo golpe a la mitad)")
            decision_combate = int(input())

            if decision_combate == 1:
                jugador.atacar(monstruo)
            elif decision_combate == 2:
                jugador.defender()
            else:
                print("Decisión inválida, turno perdido.")

            # Turno del monstruo
            if monstruo.vidas > 0:
                print(f"El {monstruo.nombre} contraataca...")
                if jugador.esta_defendiendo:
                    dano = monstruo.ataque // 2
                    print(Fore.BLUE + "¡Bloqueas la mayor parte del golpe!")
                    print(Fore.RED + f"Recibes solo {dano} de daño.")
                    jugador.vidas -= dano
                    jugador.esta_defendiendo = False
                else:
                    print(Fore.RED + "¡Recibes el golpe directo!")
                    print(Fore.RED + f"Pierdes {monstruo.ataque} de vida.")
                    jugador.vidas -= monstruo.ataque

        # Resultado del combate
        if jugador.vidas <= 0:
            print(Fore.RED + f"Has sido derrotado por el {monstruo.nombre}... Fin del juego.")
        else:
            print(Fore.GREEN + f"¡VICTORIA! Has eliminado al {monstruo.nombre}.")
            print(Fore.GREEN + "Encuentras un ¡Manual de Python!")
            print(Fore.GREEN + "Tu aventura continúa...")
    else:
        print("Te quedaste paralizado por la indecisión y un conejo te robó.")
        print("Fin del juego.")

    print("------------------------------------------------")
    print(f"Fin de la demo. Gracias por jugar, {jugador.nombre}.")

if __name__ == "__main__":
    main()