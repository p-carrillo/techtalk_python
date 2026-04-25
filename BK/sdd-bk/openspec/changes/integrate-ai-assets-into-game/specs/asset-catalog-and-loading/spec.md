## ADDED Requirements

### Requirement: Catalogo canonico de assets
El sistema SHALL definir un catalogo centralizado de assets jugables que mapee identificadores estables a rutas de archivo, incluyendo jugador, enemigos, proyectiles, escudos, explosiones, power-ups y fondos.

#### Scenario: Registro de sprites base
- **WHEN** el juego inicializa el catalogo de assets
- **THEN** cada `asset_id` requerido por gameplay y UI queda disponible con una ruta resoluble sin hardcodes en escenas

#### Scenario: Registro de backgrounds disponibles
- **WHEN** se consulta el catalogo de fondos
- **THEN** se devuelve un conjunto de backgrounds permitidos para seleccion en configuracion

### Requirement: Carga robusta mediante AssetManager
El sistema MUST cargar assets exclusivamente a traves de `AssetManager`, con cache interna y manejo de error controlado para archivos inexistentes o invalidos.

#### Scenario: Carga exitosa desde cache vacia
- **WHEN** una vista solicita por primera vez un `asset_id` valido
- **THEN** `AssetManager` carga el archivo, lo cachea y retorna la surface resultante

#### Scenario: Reuso desde cache
- **WHEN** una vista solicita nuevamente el mismo `asset_id`
- **THEN** `AssetManager` retorna la instancia cacheada sin recargar desde disco

#### Scenario: Fallback por archivo faltante
- **WHEN** un `asset_id` apunta a una ruta inexistente o no legible
- **THEN** `AssetManager` retorna un recurso fallback seguro y emite un warning accionable

### Requirement: Ruta canonica de assets en el paquete del juego
El sistema MUST resolver la ruta base de assets usando `src/space_invaders/assets` como origen unico para recursos de runtime.

#### Scenario: Ejecucion con estructura oficial
- **WHEN** existen assets en `src/space_invaders/assets`
- **THEN** la resolucion de assets funciona sin depender de carpetas externas al paquete del juego

#### Scenario: Falta de recurso en ruta canonica
- **WHEN** un archivo requerido no existe en `src/space_invaders/assets`
- **THEN** `AssetManager` aplica fallback y emite warning sin romper contratos de escenas ni vistas
