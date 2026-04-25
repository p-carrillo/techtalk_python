## Context

El proyecto ya dispone de `AssetManager`, escenas y vistas separadas por arquitectura MVC, pero no existe una especificacion formal para usar assets dentro de la estructura oficial del juego. La integracion debe mantener el contrato `input -> update -> render`, evitar acoplar logica de negocio al render y proteger el runtime ante rutas faltantes o archivos corruptos.

El cambio define como fuente unica `src/space_invaders/assets`, eliminando dependencia funcional de carpetas auxiliares de documentacion.

## Goals / Non-Goals

**Goals:**
- Definir un catalogo unico de assets jugables (sprites y backgrounds) para el juego.
- Cargar assets a traves de `AssetManager` con fallback seguro y trazabilidad de errores.
- Aplicar assets por escena/vista sin mezclar logica de dominio con renderizado.
- Permitir seleccionar fondo activo por configuracion sin tocar codigo de gameplay.
- Garantizar cobertura de tests para carga de assets y binding en escenas.

**Non-Goals:**
- No redisenar mecanicas de juego, balance o IA enemiga.
- No introducir un pipeline externo de empaquetado de arte.
- No cambiar el modelo de persistencia SQLite salvo configuraciones ya existentes.
- No añadir nuevos tipos de entidad fuera de las ya definidas en arquitectura.

## Decisions

1. Catalogo declarativo de assets en capa `core`
- Decision: crear un mapeo canonico de `asset_id -> ruta relativa` en configuracion/constantes y consumirlo desde `AssetManager`.
- Rationale: evita hardcodes dispersos en escenas y mantiene bajo acoplamiento.
- Alternativa considerada: cargar por rutas directas en cada vista; se descarta por duplicacion y baja testabilidad.

2. Ruta canonica dentro del paquete del juego
- Decision: usar `src/space_invaders/assets` como raiz unica para carga de recursos visuales.
- Rationale: mantiene coherencia con `ARCHITECTURE.md` y evita acoplamiento con carpetas externas al runtime del juego.
- Alternativa considerada: cargar desde `.ai`; se descarta por ser una carpeta de documentacion/contexto, no de runtime.

3. Fallback visual obligatorio
- Decision: si un asset no carga, usar placeholder seguro (surface simple o sprite por defecto) y registrar warning.
- Rationale: evita crash en runtime y permite seguir jugando/testeando.
- Alternativa considerada: fallo duro al cargar; se descarta porque perjudica robustez y DX.

4. Binding en vistas/escenas, no en modelos
- Decision: `GameView`, `MenuView` y escenas consumirán `asset_id`/surface resuelta sin mover reglas de entidades.
- Rationale: respeta MVC y mantiene modelos puros.
- Alternativa considerada: entidades con referencia a sprites; se descarta por mezclar dominio con infraestructura de render.

5. Validacion por tests unitarios e integracion
- Decision: cubrir carga/fallback de `AssetManager` y validar que transiciones de escenas mantienen render funcional con assets activos.
- Rationale: minimiza regresiones y alinea con `TEST.md`.
- Alternativa considerada: validacion manual; se descarta por fragilidad y baja repetibilidad.

## Risks / Trade-offs

- [Assets no presentes aun en `src/space_invaders/assets`] -> Mitigacion: tarea explicita de copiado/curacion de recursos + fallback de runtime.
- [Incremento de memoria por surfaces cacheadas] -> Mitigacion: cache controlada por `AssetManager` y carga lazy cuando sea viable.
- [Fallbacks oculten errores reales] -> Mitigacion: logging de warning con `asset_id` y ruta intentada, mas test de cobertura de errores.
- [Cambios visuales alteren legibilidad del gameplay] -> Mitigacion: criterios de contraste/tamano y validacion en pruebas de escena.
