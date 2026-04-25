#!/usr/bin/env python3
"""
Space Invaders Clone
Un clon clásico del juego Space Invaders usando Pygame
"""

import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Space Invaders")
reloj = pygame.time.Clock()

# Fuentes
fuente_grande = pygame.font.Font(None, 74)
fuente_mediana = pygame.font.Font(None, 36)
fuente_pequena = pygame.font.Font(None, 24)


class Jugador(pygame.sprite.Sprite):
    """Nave del jugador"""
    
    def __init__(self):
        super().__init__()
        self.ancho = 50
        self.alto = 40
        self.image = pygame.Surface((self.ancho, self.alto))
        self.image.fill(NEGRO)
        # Dibujar la nave
        pygame.draw.polygon(self.image, VERDE, [
            (25, 0), (50, 40), (0, 40)
        ])
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad = 5
        
    def update(self):
        """Actualizar posición del jugador"""
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
            
    def disparar(self):
        """Crear un disparo"""
        return Disparo(self.rect.centerx, self.rect.top)


class Alien(pygame.sprite.Sprite):
    """Enemigo alien"""
    
    def __init__(self, x, y):
        super().__init__()
        self.ancho = 40
        self.alto = 30
        self.image = pygame.Surface((self.ancho, self.alto))
        self.image.fill(NEGRO)
        # Dibujar el alien
        pygame.draw.rect(self.image, ROJO, (5, 10, 30, 15))
        pygame.draw.rect(self.image, ROJO, (0, 15, 40, 10))
        pygame.draw.rect(self.image, ROJO, (10, 0, 20, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def disparar(self):
        """El alien dispara"""
        return DisparoAlien(self.rect.centerx, self.rect.bottom)


class Disparo(pygame.sprite.Sprite):
    """Disparo del jugador"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(AMARILLO)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad = -10
        
    def update(self):
        """Mover el disparo hacia arriba"""
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()


class DisparoAlien(pygame.sprite.Sprite):
    """Disparo del alien"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.velocidad = 5
        
    def update(self):
        """Mover el disparo hacia abajo"""
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.kill()


class GrupoAliens:
    """Gestiona el grupo de aliens"""
    
    def __init__(self):
        self.aliens = pygame.sprite.Group()
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        self.velocidad_x = 2
        self.velocidad_descenso = 30
        self.crear_oleada()
        
    def crear_oleada(self):
        """Crear una oleada de aliens"""
        self.aliens.empty()
        for fila in range(5):
            for columna in range(11):
                x = 100 + columna * 60
                y = 50 + fila * 50
                alien = Alien(x, y)
                self.aliens.add(alien)
                
    def update(self):
        """Actualizar posición de todos los aliens"""
        # Verificar si algún alien toca el borde
        cambiar_direccion = False
        for alien in self.aliens:
            if alien.rect.right >= ANCHO and self.direccion == 1:
                cambiar_direccion = True
                break
            elif alien.rect.left <= 0 and self.direccion == -1:
                cambiar_direccion = True
                break
                
        # Cambiar dirección y descender si es necesario
        if cambiar_direccion:
            self.direccion *= -1
            for alien in self.aliens:
                alien.rect.y += self.velocidad_descenso
                
        # Mover aliens horizontalmente
        for alien in self.aliens:
            alien.rect.x += self.velocidad_x * self.direccion
            
    def disparar_aleatorio(self):
        """Un alien aleatorio dispara"""
        if self.aliens and random.randint(0, 100) < 2:  # 2% de probabilidad
            alien = random.choice(list(self.aliens))
            return alien.disparar()
        return None
        
    def draw(self, superficie):
        """Dibujar todos los aliens"""
        self.aliens.draw(superficie)
        
    def __len__(self):
        return len(self.aliens)


class Juego:
    """Clase principal del juego"""
    
    def __init__(self):
        self.jugador = Jugador()
        self.todos_sprites = pygame.sprite.Group()
        self.todos_sprites.add(self.jugador)
        
        self.grupo_aliens = GrupoAliens()
        self.disparos = pygame.sprite.Group()
        self.disparos_aliens = pygame.sprite.Group()
        
        self.puntuacion = 0
        self.vidas = 3
        self.nivel = 1
        self.juego_terminado = False
        self.victoria = False
        
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cooldown_disparo = 300  # milisegundos
        
    def manejar_eventos(self):
        """Manejar eventos del juego"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_SPACE and not self.juego_terminado:
                    # Disparar con cooldown
                    ahora = pygame.time.get_ticks()
                    if ahora - self.ultimo_disparo > self.cooldown_disparo:
                        disparo = self.jugador.disparar()
                        self.disparos.add(disparo)
                        self.todos_sprites.add(disparo)
                        self.ultimo_disparo = ahora
                elif evento.key == pygame.K_r and self.juego_terminado:
                    # Reiniciar juego
                    self.__init__()
        return True
        
    def actualizar(self):
        """Actualizar el estado del juego"""
        if self.juego_terminado:
            return
            
        # Actualizar sprites
        self.todos_sprites.update()
        self.grupo_aliens.update()
        self.disparos_aliens.update()
        
        # Aliens disparan
        disparo_alien = self.grupo_aliens.disparar_aleatorio()
        if disparo_alien:
            self.disparos_aliens.add(disparo_alien)
            
        # Colisiones: disparos del jugador con aliens
        colisiones = pygame.sprite.groupcollide(
            self.disparos, self.grupo_aliens.aliens, True, True
        )
        if colisiones:
            self.puntuacion += len(colisiones) * 10
            
        # Verificar victoria
        if len(self.grupo_aliens) == 0:
            self.nivel += 1
            self.grupo_aliens.crear_oleada()
            self.grupo_aliens.velocidad_x += 0.5
            
        # Colisiones: disparos aliens con jugador
        colisiones_jugador = pygame.sprite.spritecollide(
            self.jugador, self.disparos_aliens, True
        )
        if colisiones_jugador:
            self.vidas -= 1
            if self.vidas <= 0:
                self.juego_terminado = True
                
        # Verificar si los aliens llegaron abajo
        for alien in self.grupo_aliens.aliens:
            if alien.rect.bottom >= self.jugador.rect.top:
                self.vidas = 0
                self.juego_terminado = True
                break
                
    def dibujar(self):
        """Dibujar todo en la pantalla"""
        pantalla.fill(NEGRO)
        
        # Dibujar sprites
        self.todos_sprites.draw(pantalla)
        self.grupo_aliens.draw(pantalla)
        self.disparos_aliens.draw(pantalla)
        
        # Dibujar HUD
        texto_puntuacion = fuente_pequena.render(
            f"Puntuación: {self.puntuacion}", True, BLANCO
        )
        pantalla.blit(texto_puntuacion, (10, 10))
        
        texto_vidas = fuente_pequena.render(
            f"Vidas: {self.vidas}", True, BLANCO
        )
        pantalla.blit(texto_vidas, (10, 35))
        
        texto_nivel = fuente_pequena.render(
            f"Nivel: {self.nivel}", True, BLANCO
        )
        pantalla.blit(texto_nivel, (10, 60))
        
        # Mensajes de juego terminado
        if self.juego_terminado:
            if self.victoria:
                texto_final = fuente_grande.render("¡VICTORIA!", True, VERDE)
            else:
                texto_final = fuente_grande.render("GAME OVER", True, ROJO)
            rect_texto = texto_final.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            pantalla.blit(texto_final, rect_texto)
            
            texto_reiniciar = fuente_mediana.render(
                "Presiona R para reiniciar", True, BLANCO
            )
            rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO // 2, ALTO // 2 + 20))
            pantalla.blit(texto_reiniciar, rect_reiniciar)
            
        pygame.display.flip()
        
    def ejecutar(self):
        """Bucle principal del juego"""
        ejecutando = True
        while ejecutando:
            reloj.tick(FPS)
            ejecutando = self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            
        pygame.quit()
        sys.exit()


def main():
    """Función principal"""
    print("=== SPACE INVADERS ===")
    print("Controles:")
    print("  ← → : Mover nave")
    print("  ESPACIO : Disparar")
    print("  ESC : Salir")
    print("  R : Reiniciar (cuando termina el juego)")
    print("\n¡Iniciando juego!")
    
    juego = Juego()
    juego.ejecutar()


if __name__ == "__main__":
    main()
