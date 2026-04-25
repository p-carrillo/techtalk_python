# Assets del juego

Esta carpeta contiene los recursos visuales usados en runtime por Space Invaders.

## Estructura
- `sprites/`: entidades jugables (player, enemigos, balas, power-ups).
- `backgrounds/`: fondos de escenas.
- `effects/`: explosiones, escudos y otros efectos visuales.
- `ui/`: elementos de interfaz.

## Convencion
- Todas las rutas de assets en codigo se resuelven desde `src/space_invaders/assets`.
- No usar `.ai/` como fuente de runtime; `.ai` se considera solo contexto/documentacion.
- El mapeo de `asset_id` se documenta en `ASSET_CATALOG.md`.
