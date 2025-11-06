"""
Console UI service following Single Responsibility Principle.
Handles all user interface interactions and display logic.
"""

from colorama import init, Fore, Style
from typing import Optional

# Initialize colorama
init(autoreset=True)


class ConsoleUI:
    """
    Console User Interface service.
    Responsible only for displaying information and getting user input.
    """

    @staticmethod
    def mostrar_bienvenida() -> None:
        """Display welcome message."""
        print(Fore.YELLOW + "¡Bienvenido a las cavernas de la actividad 3!")

    @staticmethod
    def solicitar_nombre_heroe() -> str:
        """
        Prompt user for hero name.

        Returns:
            Hero name entered by user
        """
        return input(Fore.YELLOW + "Introduce el nombre de tu héroe: ")

    @staticmethod
    def mostrar_estadisticas_heroe(heroe) -> None:
        """
        Display hero statistics.

        Args:
            heroe: Hero object with nombre, vidas, ataque attributes
        """
        print("------------------------------------------------")
        print(f"Hola, {heroe.nombre}. Tus estadísticas son:")
        print(f"  Vida: {heroe.vidas}")
        print(f"  Ataque: {heroe.ataque}")
        print("------------------------------------------------")

    @staticmethod
    def mostrar_menu_camino() -> None:
        """Display path selection menu."""
        print("Llegas a una bifurcación en el camino.")
        print("Un camino lleva al bosque tranquilo, el otro a una cueva oscura.")
        print(" ")
        print(Fore.YELLOW + "1. Ir por el bosque (Ruta Segura).")
        print(Fore.YELLOW + "2. Entrar a la cueva (Ruta Peligrosa).")

    @staticmethod
    def solicitar_decision_camino() -> int:
        """
        Get path choice from user.

        Returns:
            Integer choice (1 or 2)
        """
        return int(input())

    @staticmethod
    def mostrar_camino_bosque() -> None:
        """Display forest path message."""
        print("Decides tomar el camino del bosque.")
        print("Es un paseo agradable y llegas al pueblo sin incidentes.")

    @staticmethod
    def mostrar_entrada_cueva() -> None:
        """Display cave entrance message."""
        print("Con valentía, entras en la cueva oscura...")

    @staticmethod
    def mostrar_monstruo_aparece(monstruo) -> None:
        """
        Display monster appearance message.

        Args:
            monstruo: Monster object with nombre attribute
        """
        print(f"¡Un {monstruo.nombre} salvaje aparece!")

    @staticmethod
    def mostrar_inicio_combate() -> None:
        """Display combat start message."""
        print(Fore.YELLOW + "¡COMIENZA EL COMBATE!")

    @staticmethod
    def mostrar_estado_combate(heroe, monstruo) -> None:
        """
        Display current combat status.

        Args:
            heroe: Hero object
            monstruo: Monster object
        """
        print("--- NUEVO TURNO ---")
        print(f"Vida de {heroe.nombre}: {heroe.vidas}")
        print(f"Vida del {monstruo.nombre}: {monstruo.vidas}")
        print(" ")

    @staticmethod
    def mostrar_menu_combate() -> None:
        """Display combat action menu."""
        print(Fore.YELLOW + "¿Qué harás?")

    @staticmethod
    def mostrar_opciones_combate(heroe) -> None:
        """
        Display combat options.

        Args:
            heroe: Hero object with ataque attribute
        """
        print(Fore.YELLOW + f"1. Atacar ({heroe.ataque} de daño)")
        print(Fore.YELLOW + "2. Defenderse (reduce el próximo golpe a la mitad)")

    @staticmethod
    def solicitar_decision_combate() -> int:
        """
        Get combat choice from user.

        Returns:
            Integer choice (1 or 2)
        """
        return int(input())

    @staticmethod
    def mostrar_ataque_exitoso(atacante, defensor) -> None:
        """
        Display successful attack message.

        Args:
            atacante: Attacking character
            defensor: Defending character
        """
        print(Fore.GREEN + f"¡Atacas al {defensor.nombre} con todas tus fuerzas!")
        print(Fore.GREEN + f"Le infliges {atacante.ataque} de daño.")

    @staticmethod
    def mostrar_defensa_activada() -> None:
        """Display defense activation message."""
        print(Fore.BLUE + "Te preparas para el impacto, subiendo tu guardia.")

    @staticmethod
    def mostrar_ataque_monstruo(monstruo) -> None:
        """
        Display monster attack message.

        Args:
            monstruo: Monster object
        """
        print(f"El {monstruo.nombre} contraataca...")

    @staticmethod
    def mostrar_defensa_exitosa(dano: int) -> None:
        """
        Display successful defense message.

        Args:
            dano: Damage received after defense
        """
        print(Fore.BLUE + "¡Bloqueas la mayor parte del golpe!")
        print(Fore.RED + f"Recibes solo {dano} de daño.")

    @staticmethod
    def mostrar_dano_completo(monstruo, dano: int) -> None:
        """
        Display full damage message.

        Args:
            monstruo: Monster object
            dano: Damage received
        """
        print(Fore.RED + "¡Recibes el golpe directo!")
        print(Fore.RED + f"Pierdes {dano} de vida.")

    @staticmethod
    def mostrar_victoria(monstruo) -> None:
        """
        Display victory message.

        Args:
            monstruo: Defeated monster object
        """
        print(Fore.GREEN + f"¡VICTORIA! Has eliminado al {monstruo.nombre}.")
        print(Fore.GREEN + "Encuentras un ¡Manual de Python!")
        print(Fore.GREEN + "Tu aventura continúa...")

    @staticmethod
    def mostrar_derrota(monstruo) -> None:
        """
        Display defeat message.

        Args:
            monstruo: Monster that defeated the hero
        """
        print(Fore.RED + f"Has sido derrotado por el {monstruo.nombre}... Fin del juego.")

    @staticmethod
    def mostrar_decision_invalida() -> None:
        """Display invalid choice message."""
        print("Decisión inválida, turno perdido.")

    @staticmethod
    def mostrar_fin_juego() -> None:
        """Display game over message."""
        print("Te quedaste paralizado por la indecisión y un conejo te robó.")
        print("Fin del juego.")

    @staticmethod
    def mostrar_despedida(heroe) -> None:
        """
        Display farewell message.

        Args:
            heroe: Hero object
        """
        print("------------------------------------------------")
        print(f"Fin de la demo. Gracias por jugar, {heroe.nombre}.")