## ADDED Requirements

### Requirement: Canonical asset root inside project
The system MUST load visual assets from `src/space_invaders/assets` as the canonical runtime root and MUST NOT require `.ai` paths to run the game.

#### Scenario: Runtime resolves canonical root
- **WHEN** the game starts and `AssetManager` is initialized
- **THEN** the root path used for asset resolution points to `src/space_invaders/assets`

#### Scenario: Runtime does not depend on .ai
- **WHEN** `.ai` is unavailable in the project workspace
- **THEN** the game can still resolve configured assets from the canonical root

### Requirement: Structured asset catalog for imported files
The system SHALL organize imported assets by category with deterministic relative paths and stable file names.

#### Scenario: Background assets are categorized
- **WHEN** assets are imported from source material
- **THEN** background files are stored under `src/space_invaders/assets/backgrounds/`

#### Scenario: Sprite and effect assets are categorized
- **WHEN** assets are imported from source material
- **THEN** player, enemy, bullet, shield and power-up sprites are stored under `src/space_invaders/assets/sprites/` and explosion frames under `src/space_invaders/assets/effects/`

### Requirement: Asset access goes through AssetManager
Scenes and views MUST obtain asset surfaces through `AssetManager` APIs or keys, not via direct hardcoded file paths.

#### Scenario: View requests asset by logical key
- **WHEN** a scene or view needs to render a sprite or background
- **THEN** it requests the resource through `AssetManager` using a logical identifier

#### Scenario: Missing key handling
- **WHEN** a scene or view requests a non-existent asset key
- **THEN** `AssetManager` returns a controlled failure path (explicit exception or placeholder behavior) without crashing unrelated systems

### Requirement: Asset loading behavior is covered by tests
The test suite MUST include automated checks for path resolution and loading behavior of the canonical assets.

#### Scenario: Path resolution test
- **WHEN** tests execute against `AssetManager`
- **THEN** they verify that logical keys resolve to paths under `src/space_invaders/assets`

#### Scenario: Representative load test
- **WHEN** tests load representative assets (background and sprite)
- **THEN** loading succeeds with deterministic outcomes in local and CI runs
