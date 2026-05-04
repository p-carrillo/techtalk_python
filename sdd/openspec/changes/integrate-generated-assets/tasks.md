## 1. Asset Pack Setup

- [x] 1.1 Crear `src/space_invaders/assets/` con subdirectorios `backgrounds/`, `sprites/` y `effects/`.
- [x] 1.2 Copiar los archivos desde `.ai/asstes` a la nueva estructura canonica manteniendo nombres estables.
- [x] 1.3 Verificar inventario final de assets y eliminar referencias runtime a `.ai`.

## 2. Core Asset Loading

- [x] 2.1 Actualizar `src/space_invaders/core/asset_manager.py` para resolver rutas desde `src/space_invaders/assets`.
- [x] 2.2 Definir claves logicas de acceso para backgrounds, sprites y efectos.
- [x] 2.3 Implementar manejo controlado para claves de asset inexistentes.

## 3. Scene/View Integration

- [x] 3.1 Migrar vistas/escenas que cargan rutas directas para usar `AssetManager`.
- [x] 3.2 Integrar background, sprites de entidades y efectos de explosion en escenas relevantes.
- [x] 3.3 Validar que la integracion respeta la separacion MVC (sin logica de negocio en views).

## 4. Testing and Verification

- [x] 4.1 Anadir tests unitarios para resolucion de rutas y lookup de claves en `AssetManager`.
- [x] 4.2 Anadir test de carga representativa (al menos un background y un sprite).
- [x] 4.3 Ejecutar `pytest` y ajustar regresiones de escenas/vistas si aparecen.
