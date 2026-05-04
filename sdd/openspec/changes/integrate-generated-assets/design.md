## Context

Actualmente los recursos graficos estan en `.ai/asstes`, fuera de la estructura objetivo (`src/space_invaders/assets`) definida por arquitectura. Esto introduce riesgo de rutas inestables y dependencia de un directorio temporal. El juego ya cuenta con `AssetManager`, por lo que la integracion debe concentrarse en esa capa y mantener MVC desacoplado.

## Goals / Non-Goals

**Goals:**
- Establecer `src/space_invaders/assets/` como raiz canonica de assets del juego.
- Migrar los archivos existentes de `.ai/asstes` a una jerarquia clara por categoria.
- Centralizar la resolucion de rutas en `AssetManager` para evitar rutas hardcodeadas en escenas/vistas.
- Validar por tests que las rutas y cargas criticas funcionan de forma determinista.

**Non-Goals:**
- Redisenar gameplay, balance o mecanicas.
- Introducir nuevos formatos de assets o un pipeline externo de build.
- Cambiar persistencia SQLite o contratos de repositorios.

## Decisions

1. Raiz de assets en `src/space_invaders/assets`.
Rationale: coincide con `ARCHITECTURE.md` y evita acoplar runtime a `.ai`.
Alternative considered: mantener `.ai/asstes` como origen runtime; descartado por ser ubicacion no canonica.

2. Estructura de carpetas por tipo (`backgrounds`, `sprites`, `effects`).
Rationale: simplifica descubrimiento y escalado de contenido.
Alternative considered: estructura plana; descartado por baja mantenibilidad.

3. Carga de archivos solo via `AssetManager` con claves logicas.
Rationale: elimina duplicacion de rutas y facilita pruebas.
Alternative considered: carga directa en vistas; descartado por violar separacion de responsabilidades.

4. Compatibilidad gradual con fallback controlado durante migracion.
Rationale: permite integrar sin romper escenas existentes si aun queda alguna referencia antigua.
Alternative considered: corte total inmediato; descartado por mayor riesgo de regresion.

## Risks / Trade-offs

- [Rutas legacy en vistas/escenas] -> Mitigacion: inventario de referencias y migracion a claves de `AssetManager`.
- [Assets faltantes o nombres inconsistentes] -> Mitigacion: convencion de nombres + verificacion automatizada en tests.
- [Incremento de tiempo de carga inicial] -> Mitigacion: mantener carga lazy para recursos no criticos.

## Migration Plan

1. Crear `src/space_invaders/assets/` y subdirectorios.
2. Copiar assets desde `.ai/asstes` conservando nombres estables.
3. Actualizar `AssetManager` para resolver desde la nueva raiz.
4. Migrar referencias de vistas/escenas a claves de `AssetManager`.
5. Ejecutar tests y ajustar referencias faltantes.
6. Eliminar dependencia runtime de `.ai`.

Rollback:
- Revertir commit de migracion de assets y restaurar resolucion previa en `AssetManager`.

## Open Questions

- Se desea mantener todos los backgrounds existentes o filtrar un subset inicial?
- Se requiere soporte para variantes de resolucion por asset en esta fase?
