# TEST.md

## Objetivo
Definir estrategia de testing para asegurar regresion baja y evolutividad del juego.

## Framework y Regla General
- Framework obligatorio: **pytest**.
- Toda funcionalidad nueva debe incluir tests.
- La suite debe mantenerse en verde de forma continua.
- El diseno del codigo debe priorizar testabilidad.

## Tests Unitarios Obligatorios
Cubrir como minimo:
- modelos
- servicios
- factories
- logica de puntuacion
- colisiones
- progresion de niveles

## Tests de Integracion Obligatorios
Cubrir como minimo:
- persistencia (SQLite + repositories)
- flujo de escenas (transiciones por `SceneManager`)
- eventos internos (a traves de `EventBus`)

## Reglas de Calidad de Tests
- Un test debe validar un comportamiento observable.
- Evitar tests fragiles acoplados a detalles internos irrelevantes.
- Usar fixtures para setup repetitivo.
- Simular dependencias externas cuando proceda (audio, assets, IO).
- Los tests deben ser deterministas y ejecutables en local/CI.

## Politica de Cambios
- No se acepta merge de cambios funcionales sin tests asociados.
- Correcciones de bugs deben incluir test de regresion.
- Si un test se elimina, debe justificarse con reemplazo equivalente.

