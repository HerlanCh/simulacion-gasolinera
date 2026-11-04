# ==========================================================
#  SIMULACIÓN DE UNA GASOLINERA (1 cola, 1 o 2 surtidores)
#  Mismo motor que la app web: con las mismas semillas da
#  exactamente los mismos resultados.
#  Ejecutar:  python motor_simulacion.py
# ==========================================================
import math

# ===== DATOS OBSERVADOS (50 autos) =====
DATOS = {
    "tll": {"valores": [1, 2, 3, 4, 5], "frecuencias": [10, 15, 15, 7, 3]},  # minutos entre llegadas
    "ts":  {"valores": [2, 3, 4, 5, 6], "frecuencias": [5, 10, 20, 10, 5]},  # minutos de servicio
}


# ===== GENERADOR DE NÚMEROS AL AZAR =====
# Mulberry32: con la misma semilla siempre produce la misma secuencia.
# Las operaciones "& 0xFFFFFFFF" imitan los números de 32 bits de JavaScript.
def mulberry32(semilla):
    estado = semilla & 0xFFFFFFFF

    def multiplicar32(a, b):
        return (a * b) & 0xFFFFFFFF

    def siguiente_azar():
        nonlocal estado
        estado = (estado + 0x6D2B79F5) & 0xFFFFFFFF
        t = multiplicar32(estado ^ (estado >> 15), 1 | estado)
        t = ((t + multiplicar32(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return (t ^ (t >> 14)) / 4294967296  # número R entre 0 y 1

    return siguiente_azar


# ===== LA "RULETA": tabla de probabilidades =====
# Para cada valor x: O (veces observado), f = O / N (probabilidad)
# y F (probabilidad acumulada). El tramo [inf, F) es su espacio en la ruleta.
def construir_distribucion(valores, frecuencias):
    N = sum(frecuencias)
    filas = []
    acumulado = 0
    for x, O in zip(valores, frecuencias):
        inf = acumulado / N
        acumulado += O
        filas.append({"x": x, "O": O, "f": O / N, "inf": inf, "F": acumulado / N})
    media = sum(fila["x"] * fila["f"] for fila in filas)
    var_pob = sum(fila["f"] * (fila["x"] - media) ** 2 for fila in filas)
    return {"N": N, "filas": filas, "media": media, "var_muestral": var_pob * N / (N - 1)}


# ===== TRANSFORMADA INVERSA =====
# Busca el tramo de la ruleta donde cae R y devuelve su valor.
def transformada_inversa(distribucion, R):
    for fila in distribucion["filas"]:
        if R < fila["F"]:
            return fila["x"]
    return distribucion["filas"][-1]["x"]


TLL = construir_distribucion(**DATOS["tll"])
TS = construir_distribucion(**DATOS["ts"])


# ===== SIMULACIÓN DE LA GASOLINERA =====
def simular(semilla, surtidores=1, factor_servicio=1, N=100):
    azar = mulberry32(semilla)
    libre_en = [0] * surtidores   # minuto en que cada surtidor queda libre
    clientes = []
    reloj = 0                     # t = 0: la gasolinera abre vacía

    for i in range(1, N + 1):
        # 1. Sacar dos números al azar y convertirlos en tiempos con la ruleta
        r_llegada = azar()
        tll = transformada_inversa(TLL, r_llegada)
        r_servicio = azar()
        ts = transformada_inversa(TS, r_servicio) * factor_servicio

        # 2. ¿Cuándo llega?  Llegada(i) = Llegada(i-1) + Tll
        llegada = reloj + tll
        reloj = llegada

        # 3. Elegir el surtidor que se desocupa primero
        s = libre_en.index(min(libre_en))

        # 4. ¿Cuándo empieza a cargar?  Inicio(i) = max(Llegada(i), Fin(i-1))
        inicio = max(llegada, libre_en[s])
        # 5. ¿Cuánto esperó en la fila?  Espera(i) = Inicio(i) - Llegada(i)
        espera = inicio - llegada
        # 6. ¿Cuándo se va?  Fin(i) = Inicio(i) + Ts
        fin = inicio + ts
        libre_en[s] = fin

        clientes.append({"i": i, "r_llegada": r_llegada, "tll": tll, "llegada": llegada,
                         "r_servicio": r_servicio, "ts": ts, "inicio": inicio,
                         "espera": espera, "fin": fin, "surtidor": s + 1})
    return clientes


# ===== RESULTADOS DE UNA RÉPLICA =====
def resumir(clientes, surtidores=1):
    n = len(clientes)
    esperas = sorted(c["espera"] for c in clientes)
    fin_ultimo = max(c["fin"] for c in clientes)
    tiempo_ocupado = sum(c["ts"] for c in clientes)
    return {
        "espera_media": sum(esperas) / n,          # W̄q: espera promedio en la fila
        "espera_max": esperas[-1],
        "utilizacion": tiempo_ocupado / (surtidores * fin_ultimo),
        "fin_ultimo": fin_ultimo,
    }


# ===== INFERENCIA ESTADÍSTICA =====
# Valores críticos t de Student para 95 % de confianza: t(0.025, gl)
TABLA_T = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228]


def intervalo_confianza(valores, error_max=0.10):
    n = len(valores)
    media = sum(valores) / n
    S = math.sqrt(sum((x - media) ** 2 for x in valores) / (n - 1))
    t = TABLA_T[n - 2]                       # gl = n - 1
    h = t * S / math.sqrt(n)                 # semi-amplitud: el margen de error
    # Si nadie esperó (media = 0) no hay error relativo que calcular
    error_rel = h / media if media > 0 else 0
    n_estrella = math.ceil((t * S / (error_max * media)) ** 2) if media > 0 else n
    return {"n": n, "media": media, "S": S, "t": t, "h": h,
            "inf": media - h, "sup": media + h, "error_rel": error_rel, "n_estrella": n_estrella}


# ===== PROGRAMA PRINCIPAL =====
SEMILLAS = [12345, 67890, 24680, 13579, 98765, 31415, 27182, 16180, 44444, 77777]


def mostrar_intervalo(titulo, ic):
    print(f"\n{titulo}")
    print(f"  Media W̄q = {ic['media']:.2f} min   S = {ic['S']:.2f}   t = {ic['t']:.3f}   h = {ic['h']:.2f}")
    print(f"  IC 95 % = [{ic['inf']:.2f}, {ic['sup']:.2f}]   error relativo = {ic['error_rel']:.1%}   n* = {ic['n_estrella']}")


if __name__ == "__main__":
    print(f"Media Tll = {TLL['media']:.2f} min   Media Ts = {TS['media']:.2f} min   ρ = {TS['media'] / TLL['media']:.4f}")

    # Traza de los primeros 3 clientes de la réplica 1
    print(f"\nPrimeros 3 clientes (semilla {SEMILLAS[0]}):")
    for c in simular(SEMILLAS[0])[:3]:
        print(f"  Cliente {c['i']}: R={c['r_llegada']:.4f} → Tll={c['tll']}, R={c['r_servicio']:.4f} → Ts={c['ts']} | "
              f"llega {c['llegada']:g}, inicia {c['inicio']:g}, espera {c['espera']:g}, se va {c['fin']:g}")

    # Réplicas con 1 surtidor
    print("\nRéplica  Semilla  W̄q (min)  Wq máx  Utilización")
    medias = []
    for j, semilla in enumerate(SEMILLAS[:5], start=1):
        r = resumir(simular(semilla))
        medias.append(r["espera_media"])
        print(f"  {j:<6} {semilla:<8} {r['espera_media']:>8.2f} {r['espera_max']:>7.2f} {r['utilizacion']:>10.1%}")

    mostrar_intervalo("1 surtidor, n = 5:", intervalo_confianza(medias))
    mostrar_intervalo("1 surtidor, n = 10:",
                      intervalo_confianza([resumir(simular(s))["espera_media"] for s in SEMILLAS]))
    mostrar_intervalo("2 surtidores, n = 5:",
                      intervalo_confianza([resumir(simular(s, surtidores=2), 2)["espera_media"] for s in SEMILLAS[:5]]))
