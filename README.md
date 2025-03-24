# Galactic War

**Galactic War** es un juego de disparos espacial desarrollado con Python y Pygame. El proyecto fue creado con fines educativos y para que los estudiantes experimenten con las mecánicas básicas de videojuegos usando Python.

## Características Principales

- **Controles y Navegación:**
  - La nave del jugador se mueve libremente en el eje horizontal (usando las flechas izquierda y derecha del teclado) (sin colisiones con los bordes).
  - Se dispara con la barra espaciadora.
  
- **Enemigos y Bosses:**
  - Durante la fase normal, se generan grupos de 3 enemigos cada 5 segundos.
  - Cada tres grupos se generan 2 bosses con 3 disparos de resistencia.
  - Al alcanzar 1000 puntos, se detiene la generación de enemigos normales y se invoca la batalla final contra un boss final con 20 disparos de resistencia.
  - Al eliminar un boss, se otorga un crédito adicional al jugador.

- **Sistema de Puntos y Vidas:**
  - El jugador gana puntos eliminando enemigos.
  - Se restan vidas cuando un enemigo cruza la zona de la nave.
  - El juego termina (Game Over) si las vidas bajan de 0.

- **Tienda y Boosts:**
  - La tienda se accede al presionar la tecla `ESC` durante el juego (menu de pausa).
  - En la tienda se pueden comprar mejoras:
    - **Triple Disparo:** Permite disparar 3 proyectiles a la vez (compra única). Su texto se muestra en amarillo una vez adquirido.
    - **2 Vidas extra:** Se puede comprar ilimitadamente.
    - **Aumentar Poder:** Incrementa el poder del disparo (compra única).
    - **Aumentar Velocidad:** Incrementa la velocidad de la nave (compra única).

- **Pantallas Finales:**
  - **Game Over:** Se muestra cuando el jugador se queda sin vidas.
  - **Victoria:** Se muestra al derrotar al boss final en la fase final.

## Requisitos

- **Python 3.x**
- **Pygame**

## Instalación

1. Clona o descarga el repositorio.
2. Asegúrate de tener instaladas las dependencias:
   ```bash
   pip install pygame
