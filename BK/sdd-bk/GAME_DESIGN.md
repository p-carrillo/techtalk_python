# GAME_DESIGN.md

## Objetivo
Definir como debe comportarse el juego, separado de la implementacion tecnica.

## Vision de Juego
Juego arcade de naves tipo Space Invaders: el jugador controla una nave inferior, elimina oleadas enemigas y sobrevive el mayor tiempo posible con dificultad progresiva.

## Reglas del Juego
- El jugador puede desplazarse horizontalmente y disparar.
- Los enemigos avanzan por oleadas con patron coordinado.
- El jugador pierde vida al recibir impacto enemigo o permitir condiciones de fallo definidas.
- La partida termina al agotar vidas o al completarse la condicion de victoria definida para el modo.

## Loop Principal de Gameplay
1. Preparacion de oleada/estado.
2. Fase activa de combate.
3. Resolucion de impactos y puntuacion.
4. Evaluacion de victoria/derrota de fase.
5. Transicion a siguiente oleada o fin de partida.

## Sistema de Vidas
- Vidas iniciales configurables (valor por defecto recomendado: 3).
- Tras perder una vida, se aplica breve ventana de recuperacion y reposicionamiento.
- Al llegar a 0 vidas se activa `GAME_OVER`.

## Sistema de Puntuacion
- Otorgar puntos por destruir enemigos.
- Bonus por completar oleadas rapidamente o sin dano (opcional configurable).
- Registrar high scores persistentes.

## Enemigos y Oleadas
- Tipos de enemigo con comportamiento y valor de puntos diferenciados.
- Oleadas definidas por composicion, velocidad y frecuencia de disparo.
- Progresion de dificultad por aumento gradual de:
  - velocidad enemiga
  - agresividad
  - complejidad de patron

## Dificultad Progresiva
- Escala por nivel/oleada.
- Ajusta parametros sin romper legibilidad del gameplay.
- Debe mantener curva justa: retadora pero aprendible.

## Power-Ups
- Aparicion controlada por probabilidad y/o eventos.
- Efectos posibles:
  - disparo mejorado
  - escudo temporal
  - vida extra (rara)
  - ralentizacion enemiga temporal
- Duracion y stacking deben estar claramente definidas para evitar desbalance.

## Condiciones de Victoria
- Completar todas las oleadas del modo principal.
- Alternativamente, alcanzar objetivo de puntuacion en modos infinitos (si existen).

## Condiciones de Derrota
- Vidas del jugador en 0.
- Enemigos alcanzan zona critica definida del tablero.

## Controles
Mapeo canonico de acciones:
- `move_left`
- `move_right`
- `shoot`
- `pause`
- `confirm`
- `back`

## Feedback Visual y Sonoro
- Feedback inmediato al impacto, dano y destruccion.
- Claridad de estado de partida: vidas, score, nivel/oleada, pausa y game over.
- Audio diferenciado para disparos, impactos, power-ups y eventos de estado.

## Balance General
- Evitar picos de dificultad abruptos.
- Recompensar precision y gestion de riesgo.
- Mantener ritmo arcade: ventanas de tension + respiracion controlada.
- Cualquier cambio de balance debe validarse con pruebas de gameplay reproducibles.

