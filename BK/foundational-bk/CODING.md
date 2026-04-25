# CODING.md

## Objetivo
Definir las normas de codigo para mantener calidad, consistencia y mantenibilidad.

## Principios
- Aplicar principios **SOLID**.
- Seguir **PEP 8**.
- Usar `type hints` en APIs publicas y logica relevante.
- Funciones pequenas y de responsabilidad unica.
- Bajo acoplamiento y alta cohesion.
- Evitar duplicacion.
- Preferir composicion frente a herencia.
- Usar nombres claros y expresivos.
- Priorizar legibilidad sobre clever code.

## Reglas Practicas
- Evitar funciones o metodos demasiado largos; extraer colaboradores.
- Evitar estado global mutable salvo configuracion centralizada.
- Separar logica de dominio de detalles de framework/render.
- Mantener imports limpios y dependencias en direccion arquitectonica correcta.
- No introducir optimizaciones prematuras sin evidencia.

## Convenciones de Nombres
- Clases: `PascalCase`.
- Funciones y variables: `snake_case`.
- Constantes: `UPPER_SNAKE_CASE`.
- Eventos internos: `snake_case` semantico (ejemplo: `enemy_destroyed`).

## Errores y Logging
- Manejar errores en la capa adecuada; no silenciar excepciones sin accion.
- Mensajes de error deben ser accionables y orientados al contexto.
- Logging de debug no debe contaminar el flujo normal de juego.

## Criterio de Aceptacion de Codigo
- El codigo nuevo debe ser testeable.
- El codigo nuevo debe respetar `ARCHITECTURE.md`, `DATABASE.md` y `TEST.md`.
- Cambios que rompan consistencia o aumenten deuda tecnica sin justificacion se rechazan.

