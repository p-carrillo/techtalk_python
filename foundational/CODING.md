# CODING.md

## Objetivo
Establecer normas de codificacion consistentes para mantener calidad, legibilidad y mantenibilidad del proyecto.

## Principios Generales
- Aplicar principios SOLID.
- Seguir PEP 8.
- Usar `type hints` en funciones, metodos y atributos relevantes.
- Favorecer funciones pequenas con responsabilidad unica.
- Mantener bajo acoplamiento y alta cohesion.
- Evitar duplicacion de logica.
- Preferir composicion frente a herencia.
- Priorizar codigo legible sobre clever code.

## Convenciones de Diseno
- Los nombres deben ser claros, expresivos y alineados con el dominio del juego.
- Evitar clases multiproposito.
- Separar logica de dominio, infraestructura y presentacion.
- Introducir abstracciones solo cuando resuelvan una necesidad real.

## Calidad de Implementacion
- Cada modulo debe tener un objetivo preciso.
- Evitar dependencias ciclicas entre paquetes.
- Evitar estado global mutable fuera de componentes de configuracion controlados.
- Manejar errores con mensajes accionables y sin ocultar fallos.

## Type Hints
- Obligatorios en APIs internas y publicas del proyecto.
- Evitar `Any` salvo casos justificados.
- Usar tipos del dominio cuando existan (por ejemplo, estructuras para eventos, estados o comandos).

## Definicion de Codigo Aceptable
Un cambio de codigo cumple este documento cuando:
- Respeta SOLID y PEP 8.
- Mantiene responsabilidades claras por modulo.
- Es facilmente testeable.
- Evita soluciones ad hoc que degraden la arquitectura.
