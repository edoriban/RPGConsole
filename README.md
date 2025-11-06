# RPGConsole - Juego RPG Educativo

RPGConsole es una aplicación de consola que implementa un mini-juego RPG migrado desde PSeInt a Python, siguiendo los principios SOLID y las mejores prácticas de Clean Code. El proyecto demuestra una arquitectura modular con separación clara de responsabilidades.

## 🎯 Propósito Educativo

Este proyecto fue creado con fines educativos para la clase de Programación. Sirve como ejemplo práctico de:
- Migración de código entre lenguajes
- Programación Orientada a Objetos avanzada
- Arquitectura modular con separación de responsabilidades
- Patrón de Inyección de Dependencias
- Estructuras de datos eficientes
- Integración de librerías externas

## 📋 Características

- **Arquitectura Modular**: Separación clara entre modelos, servicios, UI y datos
- **Herencia y Polimorfismo**: Jerarquía de clases Personaje → Heroe/Monstruo
- **Abstracciones**: Clases abstractas y métodos para extensibilidad
- **Interfaz Mejorada**: Sistema de colores con `colorama` para mejor UX
- **Lógica Completa**: Replicación exacta del flujo del juego original
- **Turnos por Combate**: Sistema de combate por turnos con ataque/defensa

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
   python main.py
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

### Estructura del Proyecto
```
RPGConsole/
├── main.py                 # Punto de entrada de la aplicación
├── models/                 # Modelos de dominio del juego
│   ├── personaje.py        # Clase base abstracta para personajes
│   ├── heroe.py           # Implementación específica del héroe
│   └── monstruo.py        # Implementación específica de monstruos
├── services/              # Servicios de lógica de negocio
│   ├── game_service.py    # Servicio principal que orquesta el juego
│   └── combat_service.py  # Servicio que maneja la lógica de combate
├── ui/                    # Capa de interfaz de usuario
│   └── console_ui.py      # Interfaz de consola con colores
└── data/                  # Capa de acceso a datos
    └── monsters.py        # Catálogo de monstruos disponibles
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
- **Modular**: Arquitectura separada por responsabilidades
- **Orientada a Objetos**: Herencia, polimorfismo, abstracción

## 🔄 Comparación con PSeInt

| Aspecto | PSeInt Original | Python RPGConsole |
|---------|----------------|-------------------|
| Variables | Variables simples | Atributos de clase |
| Funciones | No aplicable | Métodos especializados |
| Datos | Variables individuales | Diccionarios + clases |
| UI | Texto plano | Colores con colorama |
| Modularidad | Código lineal | Arquitectura SOLID |
| Mantenibilidad | Baja | Alta (principios Clean Code) |
| Extensibilidad | Limitada | Alta (OCP + DIP) |

## 🤝 Contribuciones

Este proyecto es educativo y no acepta contribuciones externas. Fue desarrollado como parte de un ejercicio académico.

## 📄 Licencia

Este proyecto es de uso educativo exclusivamente.