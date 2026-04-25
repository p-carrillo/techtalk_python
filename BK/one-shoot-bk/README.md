# Space Invaders Clone 🚀

Un clon clásico del juego Space Invaders desarrollado en Python usando Pygame.

## Descripción

Este es un juego arcade clásico donde controlas una nave espacial en la parte inferior de la pantalla. Tu misión es destruir oleadas de invasores alienígenas antes de que lleguen a la Tierra. ¡Cuidado con sus disparos!

## Características

- ✅ Nave jugable con movimiento suave
- ✅ Oleadas de enemigos alienígenas
- ✅ Sistema de disparos para jugador y aliens
- ✅ Detección de colisiones
- ✅ Sistema de puntuación
- ✅ Múltiples vidas
- ✅ Niveles progresivos (los aliens se vuelven más rápidos)
- ✅ Pantalla de Game Over y reinicio

## Requisitos

- Python 3.6 o superior
- Pygame 2.0 o superior

## Instalación

1. Clona este repositorio o descarga los archivos:
```bash
cd upskill_python-game-one-shot
```

2. Instala las dependencias:
```bash
pip install pygame
```

O usando el archivo de requisitos:
```bash
pip install -r requirements.txt
```

## Cómo jugar

1. Ejecuta el juego:
```bash
python space_invaders.py
```

2. Controles:
   - **← →** (Flechas izquierda/derecha): Mover la nave
   - **ESPACIO**: Disparar
   - **R**: Reiniciar el juego (después de Game Over)
   - **ESC**: Salir del juego

## Objetivo del juego

- Destruye todos los aliens antes de que lleguen a tu nave
- Esquiva los disparos enemigos
- Consigue la puntuación más alta posible
- Cada alien destruido suma 10 puntos
- Tienes 3 vidas
- Los aliens se vuelven más rápidos en cada nivel

## Consejos

- Mantén el dedo en el gatillo (espacio) para disparar continuamente
- Muévete constantemente para evitar los disparos enemigos
- Intenta eliminar primero a los aliens de los bordes para reducir la velocidad de descenso
- Los aliens disparan aleatoriamente, así que mantente alerta

## Estructura del código

El juego está organizado en las siguientes clases:

- **Jugador**: Controla la nave del jugador
- **Alien**: Representa a cada enemigo individual
- **GrupoAliens**: Gestiona el comportamiento de toda la oleada de aliens
- **Disparo**: Proyectil del jugador
- **DisparoAlien**: Proyectil de los aliens
- **Juego**: Clase principal que gestiona el bucle del juego, colisiones y estado

## Personalización

Puedes modificar fácilmente varios parámetros en el código:

- **Velocidad del juego**: Cambia la constante `FPS` (línea 17)
- **Tamaño de la ventana**: Modifica `ANCHO` y `ALTO` (líneas 14-15)
- **Velocidad de la nave**: Ajusta `self.velocidad` en la clase `Jugador`
- **Dificultad**: Modifica la probabilidad de disparo de aliens en `disparar_aleatorio()`
- **Colores**: Cambia los valores RGB en las constantes de color (líneas 19-24)

## Posibles mejoras futuras

- 🎵 Añadir música y efectos de sonido
- 🛡️ Implementar escudos protectores
- 🎨 Mejorar los gráficos con sprites personalizados
- 👾 Añadir diferentes tipos de aliens con diferentes comportamientos
- 🏆 Sistema de puntuación máxima guardada
- 💫 Efectos de partículas para explosiones
- 🎮 Soporte para joystick/gamepad

## Créditos

Inspirado en el clásico Space Invaders de Taito (1978).

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

¡Diviértete jugando! 🎮
