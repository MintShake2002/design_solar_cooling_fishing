import math
import matplotlib.pyplot as plt
# =====================================================================
# 1. PARÁMETROS INICIALES Y GEOMETRÍA
# =====================================================================
# Cámara
Largo, Ancho, Alto = 2.00, 3.00, 2.00 # [m]
A_paredes = 2*(Largo*Ancho) + 2*(Largo*Alto) + 2*(Ancho*Alto) # 10.8 m²
k_pur, espesor_pur = 0.022, 0.1 # [W/m·K], [m]

# Masas y Propiedades
m_pescado = 300.0   # [kg]
m_hielo = 100.0     # [kg]
Cp_pescado = 3.6    # [kJ/kg·K]
Cp_hielo = 2.1      # [kJ/kg·K]
lambda_pcm = 330.0  # [kJ/kg] Calor latente del PCM
fs_pcm = 1.15       # Factor de seguridad para la masa del PCM
ro_pcm = 1060       # [kg/m3]Densidad del PCM E-3 PlusIce Eutectic

# Temperaturas
T_amb = 35.0        # [°C]
T_cam = 1.0         # [°C]
T_pescado_in = 25.0 # [°C] (Asumiendo que entra temperatura ambiente/fresco)
T_hielo_in = -2.0   # [°C] (El hielo entra subenfriado)
T_evap = -10.0      # [°C]

# Operación
horas_sol = 16.0     # [h] de trabajo del compresor

# Tuberías para Condensador (Cobre de 3/8")
D_o_cond = 0.0127       # [m] Exterior
D_i_cond = 0.0114554       # [m] Interior


# Tuberías para Condensador (Cobre de 1/2")
D_o_evap = 0.015875       # [m] Exterior
D_i_evap = 0.0146304       # [m] Interior

k_cobre = 386.0     # [W/m·K]
# =====================================================================
# 2. CÁLCULO DE CARGAS TÉRMICAS (Energía total a retirar)
# =====================================================================
# A. Carga por Infiltración (24h)
Q_dot_inf = (k_pur * A_paredes * (T_amb - T_cam)) / espesor_pur # [W]
E_inf_kJ = (Q_dot_inf * 24 * 3600) / 1000.0

# B. Carga de enfriamiento de producto (Pescado y Hielo)
# (Energía para llevar el pescado a 1°C y equilibrar el hielo)
E_pescado_kJ = m_pescado * Cp_pescado * (T_pescado_in - T_cam)
E_hielo_kJ = m_hielo * Cp_hielo * (T_cam - T_hielo_in)

E_total_kJ = E_inf_kJ + E_pescado_kJ + E_hielo_kJ

# Masa de PCM requerida para almacenar esta energía
m_pcm = (E_total_kJ / lambda_pcm) * fs_pcm

#Volumen ocupado por el PCM
volumen_pcm = m_pcm/ro_pcm

#Porcentaje de volumen
volumen_camara = float(Largo*Ancho*Alto)
volumen_pcm_relativo = (volumen_pcm/volumen_camara)*100

# Potencia requerida en el evaporador (6 horas de sol)
q_evap_W = (E_total_kJ * 1000.0) / (horas_sol * 3600.0)

# Potencia del Condensador
COP = 2.96
q_cond_W = q_evap_W * (1 + (1/COP))

# Flujo Másico del Refrigerante (R600a)
h_fg_r600a = 340.0 # [kJ/kg]
m_dot_ref = (q_evap_W / 1000.0) / h_fg_r600a


# =====================================================================
# 3. DISEÑO DEL CONDENSADOR (Tubo y Aleta - Flujo Cruzado)
# =====================================================================
# Temperaturas reales (incluyendo sobrecalentamiento)
T_ref_in_c, T_ref_out_c = 65.0, 40.0
T_air_in, T_air_out = 35.0, 41.0

# Factor de corrección F (Calculado analíticamente basado en la gráfica)
P = (T_air_out - T_air_in) / (T_ref_in_c - T_air_in)
R = (T_ref_in_c - T_ref_out_c) / (T_air_out - T_air_in)
F_cond = 0.94  # Extraído de la gráfica para R=4.16 y P=0.2

# LMTD
dt1_c = T_ref_in_c - T_air_out
dt2_c = T_ref_out_c - T_air_in
LMTD_cond = (dt1_c - dt2_c) / math.log(dt1_c / dt2_c)

# Resistencias térmicas
h_ref_cond = 1500.0
h_air = 65.0
eficiencia_aleta = 0.85
factor_aletas = 11.5

R_int_c = 1 / h_ref_cond
R_cond_c = (math.log(D_o_cond / D_i_cond) * D_o_cond) / (2 * k_cobre)
R_ext_c = 1 / (h_air * eficiencia_aleta * factor_aletas)

U_cond = 1 / (R_int_c + R_cond_c + R_ext_c)

A_req_cond = q_cond_W / (U_cond * LMTD_cond * F_cond)
L_tubo_cond = A_req_cond / (math.pi * D_o_cond)

# --- NUEVO CÁLCULO GEOMÉTRICO DEL BANCO DE TUBOS ---
L_paso = 0.35           #[m]
N_tubos_total = math.ceil(L_tubo_cond / L_paso)

# =====================================================================
# 4. DISEÑO DEL EVAPORADOR (Tubo Liso sumergido)
# =====================================================================
# LMTD
T_pcm_avg = 0.0 # Temperatura promedio de fase
dt1_e = T_pcm_avg - T_evap
dt2_e = T_pcm_avg - T_evap
LMTD_evap = dt1_e # Cuando dt1 == dt2
F_evap = 1.0      # Cambio de fase puro

# Resistencias térmicas
h_ref_evap = 1800.0
h_pcm = 80.0 # Baja convección/conducción del hielo PCM

R_int_e = 1 / h_ref_evap
R_cond_e = (math.log(D_o_evap / D_i_evap) * D_o_evap) / (2 * k_cobre)
R_ext_e = 1 / h_pcm

U_evap = 1 / (R_int_e + R_cond_e + R_ext_e)

A_req_evap = q_evap_W / (U_evap * LMTD_evap * F_evap)
L_tubo_evap = A_req_evap / (math.pi * D_o_evap)

# =====================================================================
# 5. PANELES FOTOVOLTAICOS
# =====================================================================

pot_elec = q_evap_W/COP  #[W] Potencia de entrada del compresor

#Consumo electrico diario
cons_elec = (pot_elec*horas_sol) # [Wh]

#DIMENSIONAMIENTO

HSP = 4.5                  # [h] Horas de sol pico
eficiencia_panel = 0.75

pot_global = cons_elec/(HSP*eficiencia_panel)   #[W] Potencia Total del Arreglo Solar

#Numero de paneles
pot_panel = 630          #[W]
num_paneles = pot_global/pot_panel

# =====================================================================
# 6. REPORTE TÉCNICO
# =====================================================================
print(f"--- CARGAS TÉRMICAS DIARIAS ---")
print(f"Energía Total requerida:   {E_total_kJ/1000:.2f} MJ/día")
print(f"Masa de PCM necesaria:     {m_pcm:.2f} kg\n")
print(f"Volumen de PCM ocupado:    {volumen_pcm_relativo:.2f}%")

print(f"--- PARÁMETROS DEL CICLO ---")
print(f"Capacidad Evaporador:      {q_evap_W:.2f} W")
print(f"Capacidad Condensador:     {q_cond_W:.2f} W")
print(f"Flujo másico Refrigerante: {m_dot_ref:.5f} kg/s\n")

print(f"--- FACTORES LMTD Y 'U' ---")
print(f"LMTD Condensador:          {LMTD_cond:.2f} °C (F = {F_cond})")
print(f"Coeficiente U Condensador: {U_cond:.2f} W/m²K")
print(f"LMTD Evaporador:           {LMTD_evap:.2f} °C (F = {F_evap})")
print(f"Coeficiente U Evaporador:  {U_evap:.2f} W/m²K\n")

print(f"--- GEOMETRÍA FINAL ---")
print(f"L. Tubo CONDENSADOR (Aletado): {L_tubo_cond:.2f} m")
print(f"Numero de tubos requeridos para el condensador: {N_tubos_total}")
print(f"L. Tubo EVAPORADOR (Liso):     {L_tubo_evap:.2f} m")
print(f" Diametro Tubo EVAPORADOR (Liso):     {A_req_evap:.2f} m")
print(f" Diametro Tubo CONDENSADOR (Aletado): {A_req_cond:.2f} m")
print(f"Numero de paneles de {pot_panel}W: {num_paneles}.2f")




data = [
    ["Capacidad del Evaporador", f"{q_evap_W:.2f}", "W"],
    ["Capacidad del Condensador", f"{q_cond_W:.2f}", "W"],
    ["Flujo Másico del Refrigerante", f"{m_dot_ref:.5f}", "kg/s"],
    ["Energía Total a Retirar (24h)", f"{E_total_kJ/1000:.2f}", "MJ/día"],
    ["Masa de PCM Necesaria", f"{m_pcm:.2f}", "kg"],
    ["Volumen relativo PCM", f"{volumen_pcm_relativo:.2f}%","-"],
    ["U Global - Condensador", f"{U_cond:.2f}", "W/m²K"],
    ["Factor F - Condensador (Flujo Cruzado)", f"{F_cond}", "-"],
    ["Longitud Total Tubo Condensador", f"{L_tubo_cond:.2f}", "m"],
    ["Total Tubos Cortados (0.35m)", f"{N_tubos_total}", "unidades"],
    ["U Global - Evaporador", f"{U_evap:.2f}", "W/m²K"],
    ["Longitud Total Tubo Evaporador (Liso)", f"{L_tubo_evap:.2f}", "m"],
    [f"Numero de paneles de {pot_panel}W",f"{num_paneles:.2f}","-"]
]

column_headers = ["Parámetro de Diseño", "Valor Calculado", "Unidad"]

# Configurar dimensiones de la figura
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.axis('tight')
ax.axis('off')

# Crear la tabla estilizada
table = ax.table(cellText=data, colLabels=column_headers, loc='center', cellLoc='left')

# Estilo de la tabla
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.5) # Escala de ancho y alto de celdas

# Pintar las cabeceras (Azul ESPOL)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#003366') # Azul oscuro institucional
    elif row % 2 == 0:
        cell.set_facecolor('#f2f2f2') # Filas alternas gris claro para legibilidad

plt.title("RESULTADOS DE DISEÑO TÉRMICO", weight='bold', pad=20, fontsize=13)

# Guardar la imagen localmente y mostrarla en pantalla
plt.savefig("tabla_resultados_diseno.png", dpi=300, bbox_inches='tight')
plt.show()