# TEST.md

## Objetivo
Definir la estrategia de testing para garantizar estabilidad, regresion controlada y evolucion segura del juego.

## Framework
- Framework obligatorio: pytest.

## Politica General
- Toda funcionalidad nueva debe incluir tests.
- La suite debe mantenerse en verde siempre.
- El codigo debe disenarse para testabilidad desde su estructura.

## Cobertura Minima de Tests Unitarios
Debe haber tests unitarios para:
- Modelos.
- Servicios.
- Factories.
- Logica de puntuacion.
- Colisiones.
- Progresion de niveles.

## Cobertura Minima de Tests de Integracion
Debe haber tests de integracion para:
- Persistencia.
- Flujo de escenas.
- Eventos internos desacoplados.

## Reglas de Diseno para Testabilidad
- Preferir dependencias inyectables en lugar de instanciacion rigida.
- Separar logica pura de efectos secundarios (I/O, audio, assets, DB).
- Evitar acoplar tests a detalles internos no contractuales.
- Priorizar tests deterministas, rapidos y con datos controlados.

## Criterios de Aceptacion
Un cambio se considera validado cuando:
- Incluye tests adecuados al alcance del cambio.
- No rompe tests existentes.
- Mantiene o mejora la confianza en comportamiento de gameplay y persistencia.
