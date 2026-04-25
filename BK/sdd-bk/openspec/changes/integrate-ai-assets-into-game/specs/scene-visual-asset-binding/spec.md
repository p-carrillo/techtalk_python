## ADDED Requirements

### Requirement: Binding visual desacoplado por escena
El sistema MUST aplicar assets a traves de vistas y escenas sin introducir dependencias de render en `models` ni mover logica de negocio fuera de su capa.

#### Scenario: Render de GameScene con sprites de catalogo
- **WHEN** `GameScene` entra en estado `PLAYING`
- **THEN** `GameView` renderiza jugador, enemigos y proyectiles usando `asset_id` del catalogo via `AssetManager`

#### Scenario: Render de escenas de UI con assets configurados
- **WHEN** se renderiza `MainMenuScene` o `PauseScene`
- **THEN** la vista correspondiente puede pintar background configurado sin alterar flujo de control de escena

### Requirement: Seleccion de background por configuracion
El sistema SHALL permitir definir el fondo activo mediante configuracion centralizada y aplicar ese fondo en tiempo de render.

#### Scenario: Background valido configurado
- **WHEN** la configuracion contiene un `background_id` valido
- **THEN** la vista usa ese fondo como capa base de render

#### Scenario: Background no valido configurado
- **WHEN** la configuracion contiene un `background_id` inexistente
- **THEN** la vista aplica un fondo fallback y registra warning sin interrumpir la partida

### Requirement: Cobertura de pruebas para integracion visual
El sistema MUST incluir pruebas automatizadas que validen carga de assets, fallback y comportamiento de render por escena en condiciones reproducibles.

#### Scenario: Test unitario de fallback de carga
- **WHEN** se ejecutan tests unitarios de `AssetManager`
- **THEN** al menos un test verifica retorno de fallback y warning ante archivo faltante

#### Scenario: Test de integracion de flujo de escenas con assets
- **WHEN** se ejecutan tests de integracion de `SceneManager`
- **THEN** la transicion entre escenas clave mantiene render operativo usando assets del catalogo
