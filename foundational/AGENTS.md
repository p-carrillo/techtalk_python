# AGENTS.md

## Proposito
Este documento define las reglas obligatorias para cualquier agente que trabaje en el proyecto Space Invaders en Python.

## Reglas Generales Obligatorias
- Todo cambio debe respetar estrictamente las directrices definidas en [ARCHITECTURE.md](./ARCHITECTURE.md), [DATABASE.md](./DATABASE.md), [CODING.md](./CODING.md), [TEST.md](./TEST.md) y [GAME_DESIGN.md](./GAME_DESIGN.md).
- Antes de implementar cambios, el agente debe revisar la documentacion de arquitectura, persistencia, estilo de codigo, testing y diseno del juego.
- Ninguna decision tecnica puede contradecir estas guias salvo indicacion explicita del mantenedor del proyecto.
- La consistencia arquitectonica tiene prioridad sobre soluciones rapidas.

## Principios de Trabajo
- Mantener separadas las responsabilidades de arquitectura, escenas, logica de juego, renderizado, input, persistencia y testing.
- Favorecer cambios pequenos, modulares y facilmente testeables.
- Evitar introducir deuda tecnica innecesaria.
- Mantener bajo acoplamiento y alta cohesion entre modulos.
- No mezclar reglas de gameplay con detalles de infraestructura.

## Flujo Minimo para Cualquier Cambio
1. Revisar los documentos fundacionales.
2. Identificar el modulo correcto para el cambio (escena, servicio, modelo, vista, controlador, repositorio, test).
3. Implementar cambios pequenos y coherentes con la arquitectura MVC adaptada a videojuegos.
4. Añadir o actualizar tests requeridos.
5. Verificar que no se rompen reglas de persistencia ni flujo de escenas.
6. Confirmar que la documentacion sigue alineada con el comportamiento actual del juego.

## Restricciones Especificas
- No acceder a base de datos fuera de repositorios.
- No realizar transiciones de escenas fuera de `SceneManager`.
- No centralizar logica de colisiones en entidades individuales.
- No introducir dependencias innecesarias o acoplamientos cruzados entre capas.

## Definicion de Hecho
Un cambio se considera completo cuando:
- Cumple las reglas de estos documentos.
- Incluye tests apropiados.
- Mantiene la suite en verde.
- No degrada la consistencia del diseno del juego ni la arquitectura base.
