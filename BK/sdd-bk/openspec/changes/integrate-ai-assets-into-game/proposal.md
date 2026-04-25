## Why

El juego ya tiene la arquitectura base y flujo de escenas, pero todavía usa renderizado sin una integración formal de assets dentro de su propia estructura. Integrarlos ahora en `src/space_invaders/assets` mejora claridad visual, validación de gameplay y deja una base estable para iterar diseño sin romper separación por capas.

## What Changes

- Crear una carpeta de assets propia del juego en `src/space_invaders/assets` con subestructura para sprites y backgrounds.
- Definir un catálogo explícito de sprites y fondos de juego basado en los archivos incluidos en la carpeta de assets del juego.
- Incorporar carga controlada de texturas en `AssetManager` con fallback seguro cuando falte un archivo.
- Conectar los assets en vistas/escenas sin mover lógica de dominio a la capa de render.
- Añadir configuración para seleccionar fondo activo y escalar assets al tamaño de render esperado.
- Documentar la convención de assets dentro del repositorio para evitar dependencias de carpetas auxiliares.
- Cubrir la integración con tests unitarios e integración para evitar regresiones visuales/funcionales.

## Capabilities

### New Capabilities
- `asset-catalog-and-loading`: Registrar, resolver y cargar de forma consistente sprites/fondos del proyecto con manejo de errores y fallback.
- `scene-visual-asset-binding`: Aplicar assets del catálogo en `GameScene` y escenas de UI respetando contratos de Scene/View y sin acoplar lógica de negocio.

### Modified Capabilities
- Ninguna.

## Impact

- Código afectado: `src/space_invaders/core/asset_manager.py`, vistas (`src/space_invaders/views/*`), escenas (`src/space_invaders/scenes/*`), y configuración (`src/space_invaders/core/settings.py` o constantes relacionadas).
- Assets y documentación: `src/space_invaders/assets` y su documentación local de mapeo.
- Testing: nuevas pruebas en `src/space_invaders/tests/` para carga de assets y renderizado desacoplado por escenas.
- Riesgos controlados: assets faltantes en runtime y fallos de carga; se mitigarán con fallback y pruebas.
