# ARCHITECTURE.md

## Objetivo
Definir la arquitectura base para un videojuego tipo Space Invaders en Python, con una estructura modular, testeable y extensible.

## Estructura de Directorios
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

## Arquitectura General
- Patron base: MVC adaptado a videojuegos.
- Flujo de juego: escenas independientes coordinadas por `SceneManager`.
- Bucle principal obligatorio: `process input` -> `update` -> `render`.
- La logica del juego debe ser independiente de FPS usando `delta_time`.

## MVC Adaptado a Videojuegos
- **Model**: estado del juego, entidades, reglas y progresion.
- **View**: renderizado, sprites, HUD, menus y efectos visuales.
- **Controller**: captura de input, coordinacion de acciones, cambios de estado y solicitudes al `SceneManager`.

Reglas MVC:
- Los modelos no deben renderizar.
- Las vistas no deben contener reglas de negocio.
- Los controladores no deben acceder directamente a persistencia.

## Sistema de Escenas
Escenas minimas obligatorias:
- `MainMenuScene`
- `GameScene`
- `PauseScene`
- `GameOverScene`
- `HighScoresScene`
- `SettingsScene`

Contrato obligatorio para cada escena:
- `enter()`
- `exit()`
- `handle_events()`
- `update(delta_time)`
- `render()`

Reglas:
- Cada escena encapsula su flujo, estado y comportamiento principal.
- Todas las transiciones entre escenas deben pasar por `SceneManager`.
- Ninguna escena debe cambiar directamente el estado interno de otra.

## Estado Interno de GameScene
`GameScene` debe manejar estos estados:
- `READY`
- `PLAYING`
- `PLAYER_DIED`
- `LEVEL_CLEARED`
- `GAME_OVER`

## Gestores y Servicios Obligatorios
- `SceneManager`
- `AssetManager`
- `AudioManager`
- `InputManager`
- `CollisionService`
- `EventBus`
- `LevelService` o `WaveService`

Responsabilidad:
- Cada gestor resuelve un dominio unico.
- Debe evitarse duplicar logica entre gestores.

## Factories Recomendadas
- `EnemyFactory`
- `BulletFactory`
- `PowerUpFactory`
- `LevelFactory`

Uso:
- Centralizar creacion de objetos complejos.
- Evitar logica de construccion distribuida por escenas o controladores.

## Entidades del Juego
Entidades minimas:
- `Player`
- `Enemy`
- `Bullet`
- `Shield`
- `Explosion`
- `PowerUp`

Reglas de entidades:
- Mantienen su estado propio.
- No gestionan persistencia.
- No controlan escenas.
- No realizan render global.
- No consultan colisiones globales por si mismas.

## Colisiones
- La deteccion y resolucion de colisiones debe centralizarse en `CollisionService`.
- Las escenas y entidades solo reportan datos necesarios (posicion, hitbox, estado).

## Input Mapping
Mapeo de acciones obligatorio:
- `move_left`
- `move_right`
- `shoot`
- `pause`
- `confirm`
- `back`

`InputManager` debe desacoplar teclas fisicas de acciones logicas.

## Eventos Internos Desacoplados
Eventos minimos:
- `enemy_destroyed`
- `player_hit`
- `score_changed`
- `level_completed`
- `game_over`

`EventBus` debe permitir comunicacion entre modulos sin dependencias directas.

## Configuracion Centralizada
La configuracion debe centralizarse en `settings.py`/`constants.py`:
- resolucion
- FPS
- volumen
- dificultad
- controles
- constantes globales

## Modo Debug Obligatorio
El modo debug debe permitir visualizar:
- FPS
- hitboxes
- escena activa
- entidades activas
- posicion del jugador

## Coordenadas Logicas vs Render
- Separar coordenadas logicas de coordenadas de renderizado.
- Cualquier conversion de espacios debe ser explicita y estar encapsulada.

## Entry Point
Punto de entrada estandar:
```bash
python -m space_invaders
```
