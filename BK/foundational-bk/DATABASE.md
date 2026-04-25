# DATABASE.md

## Objetivo
Definir la capa de persistencia para el proyecto con bajo acoplamiento y posibilidad de evolucion futura.

## Motor y Principios
- Motor de persistencia: **SQLite**.
- Acceso a datos exclusivamente mediante patron **Repository**.
- Toda operacion de persistencia debe encapsularse en repositorios.
- Queda prohibido acceder a base de datos desde escenas, modelos, vistas o controladores.
- El diseno debe permitir migrar a otro motor sin romper logica de juego.

## Datos a Persistir
- `high_scores`
- `settings`
- estadisticas basicas de partida
- progreso (si aplica al modo de juego)

## Estructura de Capa de Datos
- `repositories/` contiene interfaces y adaptadores concretos SQLite.
- `services/` orquesta casos de uso y consume repositorios.
- `models/` define entidades de dominio sin SQL embebido.

## Esquema Minimo Recomendado
- Tabla `high_scores`: id, player_name, score, wave, created_at.
- Tabla `settings`: id, key, value, updated_at.
- Tabla `player_stats`: id, games_played, enemies_destroyed, shots_fired, shots_hit, updated_at.
- Tabla `progress` (opcional): id, level, wave, lives, score, updated_at.

## Inicializacion y Migraciones
- Debe existir inicializacion automatica de esquema al arrancar si la base no existe.
- Debe existir una migracion base versionada (por ejemplo `001_initial.sql`).
- Cambios de esquema posteriores deben versionarse y ejecutarse en orden.
- Registrar version de schema (tabla `schema_migrations` o equivalente).

## Reglas Operativas
- Validar integridad en repositorios (constraints, tipos y defaults).
- Usar transacciones para escrituras compuestas.
- Manejar errores de persistencia sin filtrar detalles SQL hacia escenas.
- Mantener consultas parametrizadas para evitar inyecciones.

