# DATABASE.md

## Objetivo
Definir la estrategia de persistencia del proyecto de forma desacoplada, mantenible y preparada para evolucion futura.

## Motor de Base de Datos
- Motor obligatorio: SQLite.
- El acceso debe realizarse mediante una capa dedicada de repositorios.

## Patron de Acceso a Datos
- Patron obligatorio: Repository.
- Toda operacion de persistencia debe encapsularse en repositorios dentro de `repositories/`.
- Prohibido acceder a base de datos desde `scenes/`, `models/`, `views/` o `controllers/`.

## Recursos a Persistir
Se debe persistir como minimo:
- High scores.
- Settings del usuario.
- Estadisticas basicas de juego.
- Progreso de partida, si aplica a la implementacion final.

## Reglas de Diseno
- Diseno desacoplado para permitir migracion futura a otro motor sin romper la logica de negocio.
- Definir interfaces de repositorio cuando sea necesario para facilitar sustitucion de implementaciones.
- No mezclar SQL con logica de gameplay.
- Mantener consultas simples, legibles y con responsabilidades acotadas.

## Inicializacion y Migraciones
- Debe existir una fase de inicializacion de esquema al arrancar el sistema de persistencia.
- Debe existir una migracion basica de esquema versionada.
- Cualquier cambio de esquema debe registrarse y ser reproducible en entornos limpios.

## Integridad y Seguridad
- Usar constraints y tipos apropiados para mantener integridad de datos.
- Validar datos antes de persistirlos.
- Manejar errores de I/O y bloqueos de SQLite de forma controlada.

## Testing de Persistencia
- Cubrir repositorios con tests de integracion (lectura/escritura real en SQLite de prueba).
- Verificar creacion de esquema y migraciones basicas en tests.
