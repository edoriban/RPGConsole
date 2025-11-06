# Aventura RPG - Migración de PSeInt a Python

Este proyecto es una migración completa del mini-juego RPG originalmente creado en PSeInt (`AventuraRPG.psc`) a una aplicación funcional en Python. El objetivo es demostrar la transición de un lenguaje educativo a uno profesional, implementando conceptos de Programación Orientada a Objetos (OOP) y mejores prácticas de desarrollo.

## 🎯 Propósito Educativo

Este proyecto fue creado con fines educativos para la clase de Programación. Sirve como ejemplo práctico de:
- Migración de código entre lenguajes
- Implementación de OOP en Python
- Uso de estructuras de datos (diccionarios)
- Manejo de entrada/salida en consola
- Integración de librerías externas (colorama)

## 📋 Características

- **Arquitectura OOP**: Clase `Personaje` para manejar tanto al jugador como a los monstruos
- **Gestión de Datos**: Diccionario `catalogo_monstruos` para almacenar estadísticas de enemigos
- **Interfaz Mejorada**: Uso de colores con la librería `colorama` para una mejor experiencia visual
- **Lógica Completa**: Replicación exacta del flujo del juego original en PSeInt
- **Turnos por Combate**: Sistema de combate por turnos con opciones de ataque y defensa

## 🚀 Requisitos

- Python 3.6 o superior
- Librería `colorama` (instalable con `pip install colorama`)

## 📦 Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:
   ```bash
   pip install colorama
   ```
3. Ejecuta el juego:
   ```bash
   python aventura_rpg.py
   ```

## 🎮 Cómo Jugar

1. **Inicio**: Introduce el nombre de tu héroe
2. **Selección de Camino**:
   - Opción 1: Camino del bosque (ruta segura)
   - Opción 2: Entrar a la cueva (ruta peligrosa con combate)
3. **Combate** (solo en la cueva):
   - Elige entre Atacar (daño completo) o Defender (reduce daño recibido a la mitad)
   - El monstruo contraataca automáticamente
   - Gana derrotando al monstruo o pierde si tus vidas llegan a 0

## 🏗️ Arquitectura del Código

### Clase Personaje
```python
class Personaje:
    def __init__(self, nombre, vidas, ataque)
    def atacar(self, enemigo)
    def defender(self)
```

### Diccionario de Monstruos
```python
catalogo_monstruos = {
    "Goblin": {"vidas": 60, "ataque": 12},
    "Ogro": {"vidas": 60, "ataque": 12},
    "Orco": {"vidas": 60, "ataque": 12},
    "Slime": {"vidas": 60, "ataque": 12}
}
```

## 🎨 Colores Utilizados

- **Amarillo**: Menús y mensajes de bienvenida
- **Verde**: Ataques exitosos y mensajes de victoria
- **Azul**: Acciones de defensa
- **Rojo**: Daño recibido y mensajes de derrota

## 📚 Estructuras Implementadas

- **Secuencial**: Inicio del juego y configuración inicial
- **Selección**: Menús de decisión (camino y combate)
- **Repetitiva**: Bucle de combate por turnos

## 🔄 Comparación con PSeInt

| Aspecto | PSeInt Original | Python Migrado |
|---------|----------------|----------------|
| Variables | Variables simples | Atributos de clase |
| Funciones | No aplicable | Métodos de clase |
| Datos | Variables individuales | Diccionarios estructurados |
| UI | Texto plano | Colores con colorama |
| Modularidad | Código lineal | OOP con clases |

## 🤝 Contribuciones

Este proyecto es educativo y no acepta contribuciones externas. Fue desarrollado como parte de un ejercicio académico.

## 📄 Licencia

Este proyecto es de uso educativo exclusivamente.