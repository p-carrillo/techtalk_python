## 1. Catalogo y resolucion de assets

- [ ] 1.1 Crear estructura de carpetas en `src/space_invaders/assets` (por ejemplo: `sprites/`, `backgrounds/`, `effects/`, `ui/`).
- [ ] 1.2 Definir el catalogo canonico de `asset_id` a rutas relativas (sprites y backgrounds) en `core/constants` o `core/settings`.
- [ ] 1.3 Implementar resolucion de ruta base usando `src/space_invaders/assets` como origen unico.
- [ ] 1.4 Documentar el mapeo final de assets en una guia local dentro del propio paquete del juego.

## 2. AssetManager y manejo de fallback

- [ ] 2.1 Extender `AssetManager` para carga por `asset_id` con cache de surfaces.
- [ ] 2.2 Implementar fallback seguro para archivos faltantes/corruptos con warning accionable.
- [ ] 2.3 Añadir soporte de transformaciones de escala requeridas para render consistente.

## 3. Integracion en escenas y vistas

- [ ] 3.1 Actualizar `GameView` para renderizar player/enemies/bullets/shields/explosiones/power-ups con assets del catalogo.
- [ ] 3.2 Integrar background configurable en `MenuView` y flujo visual de escenas de UI.
- [ ] 3.3 Ajustar escenas para pasar dependencias de assets a vistas sin acoplar logica de dominio.

## 4. Configuracion y contratos

- [ ] 4.1 Incorporar `background_id` y parametros de assets relevantes en configuracion centralizada.
- [ ] 4.2 Validar que el flujo `process input -> update -> render` se mantiene sin cambios de contrato de escena.
- [ ] 4.3 Verificar que no se introducen dependencias de persistencia en capas de render/escena.

## 5. Testing y validacion

- [ ] 5.1 Crear tests unitarios para carga, cache y fallback de `AssetManager`.
- [ ] 5.2 Ampliar tests de integracion de `SceneManager` para validar render operativo con assets configurados.
- [ ] 5.3 Ejecutar `pytest` completo y corregir regresiones antes de marcar el cambio como implementado.
