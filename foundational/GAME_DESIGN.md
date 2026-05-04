# GAME_DESIGN.md

## Objetivo
Definir como debe comportarse el juego Space Invaders desde la perspectiva de diseno, separado de decisiones tecnicas de implementacion.

## Reglas del Juego
- El jugador controla una nave en la parte inferior de la pantalla.
- Debe destruir oleadas de enemigos que avanzan progresivamente.
- El jugador evita proyectiles enemigos y colisiones directas.
- Escudos ofrecen proteccion parcial y pueden degradarse.

## Loop Principal de Gameplay
- Mover jugador.
- Disparar.
- Gestionar movimiento enemigo y patrones de ataque.
- Resolver colisiones.
- Actualizar puntuacion, vidas y estado de nivel.
- Evaluar condiciones de victoria o derrota.

## Sistema de Vidas
- El jugador inicia con un numero definido de vidas (configurable).
- Perder una vida al recibir impacto valido.
- Breve ventana de recuperacion tras respawn, si se define en balance.
- Al llegar a 0 vidas se activa `GAME_OVER`.

## Puntuacion
- Destruir enemigos incrementa puntuacion segun tipo de enemigo.
- Bonus por limpiar oleada sin perder vida (opcional configurable).
- Bonus por completar nivel (si aplica).
- Tabla de high scores persistente.

## Enemigos
- Deben existir diferentes tipos con variaciones de velocidad, resistencia o patron de disparo.
- El comportamiento enemigo aumenta presion con el avance del juego.
- La formacion enemiga puede desplazarse horizontalmente y descender por fases.

## Oleadas y Progresion
- El juego avanza por oleadas o niveles.
- Cada nueva oleada incrementa dificultad de forma gradual.
- `LevelService` o `WaveService` controla composicion y progresion.

## Dificultad Progresiva
Escalar con combinacion de:
- Mayor velocidad enemiga.
- Mayor frecuencia de disparo enemigo.
- Mayor variedad de enemigos.
- Menor margen de error para el jugador.

## Power-Ups
Power-ups sugeridos:
- Disparo doble.
- Cadencia aumentada.
- Escudo temporal.
- Vida extra.

Reglas:
- Deben tener duracion o condicion clara.
- Deben estar balanceados para no romper la progresion.

## Condiciones de Victoria
- Victoria por completar todas las oleadas definidas en la sesion.
- Alternativamente, modo infinito con objetivo de maximizar puntuacion.

## Condiciones de Derrota
- Derrota al perder todas las vidas.
- Derrota opcional si enemigos alcanzan zona critica inferior.

## Controles
Mapeo logico obligatorio:
- `move_left`
- `move_right`
- `shoot`
- `pause`
- `confirm`
- `back`

## Feedback Visual y Sonoro
- Señales claras para impacto, destruccion y dano recibido.
- Indicadores visibles de vidas, puntuacion, oleada y estado.
- Audio diferenciado para disparo, colision, explosion y transiciones criticas.
- En modo debug, visualizacion opcional de hitboxes y metricas clave.

## Balance General de Gameplay
- El juego debe ser desafiante pero legible.
- Evitar picos bruscos de dificultad sin telemetria o ajuste gradual.
- El jugador debe poder aprender patrones y mejorar por habilidad.
- Ajustes de dificultad deben impactar ritmo, no solo penalizacion.
