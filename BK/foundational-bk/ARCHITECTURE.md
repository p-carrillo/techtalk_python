# ARCHITECTURE.md

## Objetivo
Definir la arquitectura base del proyecto para un videojuego tipo Space Invaders en Python, con MVC adaptado a videojuegos y gestion de escenas desacoplada.

## Arquitectura Base
- Patron principal: **MVC adaptado a videojuegos**.
- Flujo de runtime obligatorio: `process input -> update -> render`.
- Toda logica de juego debe ser independiente del FPS mediante `delta_time`.

## Estructura de Directorios Objetivo
```text
src/
└── space_invaders/
    ├── main.py
    ├── core/
    │   ├── game.py
    │   ├── scene.py
    │   ├── scene_manager.py
    │   ├── asset_manager.py
    │   ├── audio_manager.py
    │   ├── input_manager.py
    │   ├── event_bus.py
    │   ├── settings.py
    │   └── constants.py
    ├── scenes/
    ├── models/
    ├── views/
    ├── controllers/
    ├── services/
    ├── factories/
    ├── repositories/
    ├── assets/
    └── tests/
```

## Entry Point Estandar
```bash
python -m space_invaders
```

## Escenas y SceneManager
- Toda transicion entre escenas debe pasar por `SceneManager`.
- Cada escena encapsula su flujo, estado y comportamiento principal.
- Escenas minimas obligatorias:
  - `MainMenuScene`
  - `GameScene`
  - `PauseScene`
  - `GameOverScene`
  - `HighScoresScene`
  - `SettingsScene`

### Contrato de Escena
Cada escena debe implementar:
- `enter()`
- `exit()`
- `handle_events()`
- `update(delta_time)`
- `render()`

## Separacion MVC
- **Model**: estado del juego, entidades, reglas y simulacion.
- **View**: renderizado, sprites, HUD, menus y efectos visuales.
- **Controller**: input, coordinacion de acciones y cambios de escena.

## Sistemas y Gestores Obligatorios
- `SceneManager`
- `AssetManager`
- `AudioManager`
- `InputManager`
- `CollisionService`
- `EventBus`
- `LevelService` y/o `WaveService`

## Factories Recomendadas
- `EnemyFactory`
- `BulletFactory`
- `PowerUpFactory`
- `LevelFactory`

## Entidades del Juego
Entidades minimas:
- `Player`
- `Enemy`
- `Bullet`
- `Shield`
- `Explosion`
- `PowerUp`

Reglas de entidad:
- Mantienen su estado.
- No gestionan persistencia.
- No controlan escenas.
- No realizan render global.
- No consultan colisiones globales por si mismas.

## Colisiones
- La deteccion y resolucion de colisiones debe estar centralizada en `CollisionService`.
- Ninguna entidad debe resolver colisiones globales de forma directa.

## Input Mapping Canonico
- `move_left`
- `move_right`
- `shoot`
- `pause`
- `confirm`
- `back`

## Eventos Internos Desacoplados
- `enemy_destroyed`
- `player_hit`
- `score_changed`
- `level_completed`
- `game_over`

Los eventos deben propagarse via `EventBus`.

## Estados Internos de GameScene
`GameScene` debe modelar explicitamente:
- `READY`
- `PLAYING`
- `PLAYER_DIED`
- `LEVEL_CLEARED`
- `GAME_OVER`

## Configuracion Centralizada
Debe existir una configuracion comun para:
- resolucion
- FPS
- volumen
- dificultad
- controles
- constantes globales

## Modo Debug Obligatorio
Debe permitir visualizar como minimo:
- FPS
- hitboxes
- escena activa
- entidades activas
- posicion del jugador

## Coordenadas
Separar:
- coordenadas logicas (simulacion)
- coordenadas de renderizado (presentacion)

## Reglas de Dependencias
- `scenes` puede depender de `controllers`, `services` y `core`.
- `models` no depende de `views`.
- `views` no modifica estado de negocio directamente.
- `repositories` solo es consumido por `services` de aplicacion.
- `core` define contratos y orquestacion, evitando conocer detalles de dominio concreto cuando no sea necesario.

