## Why

Los assets visuales existen actualmente en `.ai/asstes`, que es una ubicacion temporal y fuera de la estructura objetivo del juego. Necesitamos incorporarlos en una carpeta de `assets` del proyecto para que la carga en runtime sea estable, mantenible y alineada con la arquitectura.

## What Changes

- Crear la carpeta `src/space_invaders/assets/` como origen canonico de recursos graficos del juego.
- Copiar los archivos existentes desde `.ai/asstes` a la nueva estructura de `assets`, organizados por tipo (backgrounds, sprites, effects).
- Definir convenciones de nombres y rutas para que `AssetManager` cargue los recursos desde el proyecto y no desde `.ai`.
- Integrar los nuevos assets en las vistas/escenas relevantes sin romper el contrato MVC ni la separacion de capas.
- Cubrir con tests la resolucion de rutas y carga de assets para prevenir regresiones.

## Capabilities

### New Capabilities
- `project-asset-pack`: Gestion estandarizada de assets dentro de `src/space_invaders/assets` con carga centralizada desde `AssetManager`.

### Modified Capabilities
- Ninguna.

## Impact

- Codigo afectado: `src/space_invaders/core/asset_manager.py`, vistas y/o escenas que referencian recursos, y tests en `src/space_invaders/tests`.
- Estructura afectada: alta de `src/space_invaders/assets/` con subdirectorios por categoria.
- Dependencias: sin nuevas dependencias externas.
- Riesgo principal: rutas hardcodeadas antiguas; mitigacion con centralizacion en `AssetManager` y tests de carga.
