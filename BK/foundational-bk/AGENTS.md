# AGENTS.md

## Proposito
Establecer las normas obligatorias para cualquier agente (humano o automatizado) que modifique este proyecto de Space Invaders en Python.

## Fuentes de Verdad
Todo cambio debe alinearse con estos documentos:
- `AGENTS.md`
- `ARCHITECTURE.md`
- `DATABASE.md`
- `CODING.md`
- `TEST.md`
- `GAME_DESIGN.md`

## Reglas Obligatorias
1. Todo cambio debe respetar estrictamente las directrices establecidas en las foundational files.
2. Antes de implementar, el agente debe revisar arquitectura, persistencia, estilo de codigo, testing y diseno de juego.
3. Ninguna decision tecnica puede contradecir estas guias salvo indicacion explicita del solicitante.
4. Mantener separadas las responsabilidades de arquitectura, escenas, logica de juego, renderizado, input, persistencia y testing.
5. Favorecer cambios pequenos, modulares y facilmente testeables.
6. Evitar introducir deuda tecnica innecesaria.
7. Priorizar consistencia arquitectonica sobre soluciones rapidas.

## Flujo de Trabajo Minimo
1. Revisar requisitos funcionales y `GAME_DESIGN.md`.
2. Verificar impacto arquitectonico en `ARCHITECTURE.md`.
3. Verificar impacto en persistencia con `DATABASE.md`.
4. Implementar siguiendo `CODING.md`.
5. Anadir o actualizar tests segun `TEST.md`.
6. Validar que el cambio no rompe separacion de capas ni contratos de escenas.

## Limites de Decision
- Si una tarea exige romper una regla de estos documentos, se debe escalar y pedir aprobacion explicita antes de implementar.
- Si hay conflicto entre rapidez y arquitectura, gana la arquitectura.
- Si una solucion incrementa acoplamiento o reduce testabilidad sin motivo de peso, debe rechazarse.

