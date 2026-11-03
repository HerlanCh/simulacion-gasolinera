# Simulación de una gasolinera

**Ver la app:** https://herlanch.github.io/simulacion-gasolinera/

## ¿De qué trata?

Una gasolinera tiene **un solo surtidor** y los autos hacen **una sola fila** (el primero que llega es el primero en ser atendido).

- En promedio llega un auto cada **2.56 minutos**.
- Atender a cada auto toma en promedio **4.00 minutos**.

Llegan autos más rápido de lo que se pueden atender, así que la fila crece sin parar. Esta app lo demuestra con datos y con una simulación por computadora, y compara qué pasaría con **un segundo surtidor**.

## Cómo usarla

Abre el enlace de arriba o haz doble clic en `index.html`. No hay que instalar nada.

La app tiene 5 secciones:

| Sección | Qué muestra |
|---|---|
| Planteamiento | El problema y el resultado principal |
| Módulo 1 · Datos | Las tablas de datos, la prueba χ² y cómo un número al azar se convierte en minutos |
| Módulo 2 · Simulador | Una animación de los 100 autos llegando y esperando, paso a paso |
| Módulo 3 · Réplicas | Repetir la simulación varias veces y calcular cuánto confiar en el resultado |
| Módulo 4 · Preguntas | Respuestas a las preguntas del trabajo, con las cifras simuladas |

Atajos: las teclas `0`–`4` cambian de sección. En el simulador, `Espacio` reproduce o pausa y `→` avanza un evento.

## Datos usados (50 observaciones)

| Minutos entre llegadas | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Veces observado | 10 | 15 | 15 | 7 | 3 |

| Minutos de atención | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| Veces observado | 5 | 10 | 20 | 10 | 5 |

## Archivos

- `index.html`: la app completa (HTML, CSS y JavaScript en un solo archivo).
- `motor_simulacion.py`: el mismo motor de simulación en Python. Con las mismas semillas da exactamente los mismos resultados que la app. Se ejecuta con `python motor_simulacion.py` (no necesita instalar librerías).
- `PRODUCT.md` y `DESIGN.md`: notas sobre el propósito y el diseño visual.
