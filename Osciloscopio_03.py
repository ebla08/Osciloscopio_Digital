#Osciloscopio --> Barrios Quiroga Edward
import threading
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import csv
from datetime import datetime
import numpy as np
from matplotlib.widgets import Button, Slider

#____________________________________________________________________________________________________________________________________________
# Configurar estilo oscuro
plt.style.use('dark_background')

# Configuración del puerto serie
PUERTO = 'COM3'  # Ajustar según tu sistema
VELOCIDAD = 115200

# Abrimos el puerto serial
ser = serial.Serial(PUERTO, VELOCIDAD, timeout=1)
ser.reset_input_buffer()
#____________________________________________________________________________________________________________________________________________
# Buffers de datos para cuatro canales
BUFFER_SIZE = 200
valores_ch0 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
valores_ch1 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
valores_ch2 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
valores_ch3 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)

# Estado de los canales (activado/desactivado)
canales_activos = [True, True, True, True]
pausado = False
guardar_datos = False
datos_guardados = []

#____________________________________________________________________________________________________________________________________________
buffer_lock = threading.Lock()
#____________________________________________________________________________________________________________________________________________
# Hilo de lectura del puerto serial
def leer_serial():
    while True:
        try:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            partes = linea.split(',')
            if len(partes) == 4 and all(p.replace('-', '').isdigit() for p in partes):
                ch0, ch1, ch2, ch3 = map(int, partes)
                with buffer_lock:
                    if not pausado:
                        valores_ch0.append(ch0)
                        valores_ch1.append(ch1)
                        valores_ch2.append(ch2)
                        valores_ch3.append(ch3)
                        if guardar_datos:
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                            datos_guardados.append([timestamp, ch0, ch1, ch2, ch3])
        except Exception as e:
            print("Error en lectura serial:", e)
#____________________________________________________________________________________________________________________________________________
# Lanzar el hilo como daemon
hilo = threading.Thread(target=leer_serial, daemon=True)
hilo.start()

# Crear figura con subplots personalizados
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('black')

# Layout personalizado - displays más pequeños
gs = fig.add_gridspec(3, 4, height_ratios=[0.4, 3, 0.8], width_ratios=[1, 1, 1, 1])
#____________________________________________________________________________________________________________________________________________
# Panel principal del osciloscopio
ax_main = fig.add_subplot(gs[1, :])
ax_main.set_facecolor('#111111')
#____________________________________________________________________________________________________________________________________________
# Paneles para displays digitales
ax_display1 = fig.add_subplot(gs[0, 0])
ax_display2 = fig.add_subplot(gs[0, 1])
ax_display3 = fig.add_subplot(gs[0, 2])
ax_display4 = fig.add_subplot(gs[0, 3])
#____________________________________________________________________________________________________________________________________________
# Configurar displays digitales - más compactos
displays = [ax_display1, ax_display2, ax_display3, ax_display4]
colores = ['#00ffff', '#ff6600', '#00ff00', '#ff00ff']
nombres_canales = ['CH1', 'CH2', 'CH3', 'CH4']

for i, ax_disp in enumerate(displays):
    ax_disp.set_facecolor('#1a1a1a')
    ax_disp.set_xlim(0, 1)
    ax_disp.set_ylim(0, 1)
    ax_disp.set_xticks([])
    ax_disp.set_yticks([])
    for spine in ax_disp.spines.values():
        spine.set_color(colores[i])
        spine.set_linewidth(1.5)
#____________________________________________________________________________________________________________________________________________
# Textos para displays digitales - más minimalistas
display_texts = []
for i, ax_disp in enumerate(displays):
    ax_disp.text(0.5, 0.75, nombres_canales[i], ha='center', va='center', 
                 color=colores[i], fontsize=8, fontweight='bold', transform=ax_disp.transAxes)
    text_valor = ax_disp.text(0.5, 0.35, '0000', ha='center', va='center', 
                             color='white', fontsize=12, fontweight='bold', 
                             transform=ax_disp.transAxes, family='monospace')
    display_texts.append(text_valor)

# Precompute x-axis data
x_data = np.arange(BUFFER_SIZE)
#____________________________________________________________________________________________________________________________________________
# Líneas para los cuatro canales - más suaves
linea_ch0, = ax_main.plot(x_data, list(valores_ch0), color=colores[0], linewidth=1.5, label='Canal 1')
linea_ch1, = ax_main.plot(x_data, list(valores_ch1), color=colores[1], linewidth=1.5, label='Canal 2')
linea_ch2, = ax_main.plot(x_data, list(valores_ch2), color=colores[2], linewidth=1.5, label='Canal 3')
linea_ch3, = ax_main.plot(x_data, list(valores_ch3), color=colores[3], linewidth=1.5, label='Canal 4')
#____________________________________________________________________________________________________________________________________________
# Configuración del gráfico principal
ax_main.set_ylim(0, 4095)
ax_main.set_xlim(0, BUFFER_SIZE)
ax_main.set_title("Osciloscopio Digital - 4 Canales", color='white', fontsize=16, fontweight='bold')
ax_main.set_ylabel("Valores ADC (0-4095)", color='lightgray', fontsize=12)
ax_main.set_xlabel("Muestras", color='lightgray', fontsize=12)
ax_main.grid(True, color='#333333', linewidth=0.5, alpha=0.7)
#____________________________________________________________________________________________________________________________________________
# Personalizar bordes del gráfico principal
for spine in ax_main.spines.values():
    spine.set_color('#666666')

ax_main.tick_params(colors='lightgray')
#____________________________________________________________________________________________________________________________________________
# Leyenda
legend = ax_main.legend(loc="upper right", facecolor=(0.2, 0.2, 0.2, 0.8), edgecolor='#666666')
for text in legend.get_texts():
    text.set_color('white')
#____________________________________________________________________________________________________________________________________________
# Botones (ajustados para el nuevo layout)
ax_pause = plt.axes([0.85, 0.02, 0.08, 0.04])
ax_save = plt.axes([0.85, 0.07, 0.08, 0.04])
ax_ch0 = plt.axes([0.75, 0.02, 0.08, 0.04])
ax_ch1 = plt.axes([0.75, 0.07, 0.08, 0.04])
ax_ch2 = plt.axes([0.65, 0.02, 0.08, 0.04])
ax_ch3 = plt.axes([0.65, 0.07, 0.08, 0.04])
ax_reset = plt.axes([0.85, 0.12, 0.08, 0.04])

btn_pause = Button(ax_pause, 'Pausa', color=(0.1, 0.1, 0.3, 0.7), hovercolor='#00E1FF')
btn_save = Button(ax_save, 'Guardar', color=(0.1, 0.1, 0.3, 0.7), hovercolor='#FF3D00')
btn_ch0 = Button(ax_ch0, 'CH1', color=(0.05, 0.05, 0.15, 0.7), hovercolor=colores[0])
btn_ch1 = Button(ax_ch1, 'CH2', color=(0.05, 0.05, 0.15, 0.7), hovercolor=colores[1])
btn_ch2 = Button(ax_ch2, 'CH3', color=(0.05, 0.05, 0.15, 0.7), hovercolor=colores[2])
btn_ch3 = Button(ax_ch3, 'CH4', color=(0.05, 0.05, 0.15, 0.7), hovercolor=colores[3])
btn_reset = Button(ax_reset, 'Reiniciar', color=(0.1, 0.1, 0.3, 0.7), hovercolor='#00E1FF')
#____________________________________________________________________________________________________________________________________________
# botones
for btn in [btn_pause, btn_save, btn_ch0, btn_ch1, btn_ch2, btn_ch3, btn_reset]:
    btn.label.set_fontsize(9)
    btn.label.set_color('#E0E0FF')
    btn.label.set_fontweight('medium')
#____________________________________________________________________________________________________________________________________________
# Slider para escala Y
ax_scale = plt.axes([0.1, 0.02, 0.3, 0.03])
slider_scale = Slider(ax_scale, 'Escala Y', 100, 4095, valinit=4095, valstep=100,
                      color='#00E1FF', handle_style={'facecolor': '#E0E0FF', 'edgecolor': '#00E1FF', 'size': 12})

ax_scale.set_facecolor((0.1, 0.1, 0.3, 0.7))
ax_scale.tick_params(colors='#B0B0FF')

# Leyenda Vpp 
vpp_legend_ax = plt.axes([0.06, 0.73, 0.15, 0.1])
vpp_legend_ax.patch.set_facecolor((0.2, 0.2, 0.2, 0.8))
vpp_legend_ax.patch.set_edgecolor('#666666')
vpp_legend_ax.set_xticks([])
vpp_legend_ax.set_yticks([])

vpp_texts = [
    vpp_legend_ax.text(0.05, 0.75, f'CH1: Vpp=0.0', color=colores[0], fontsize=10, transform=vpp_legend_ax.transAxes),
    vpp_legend_ax.text(0.05, 0.55, f'CH2: Vpp=0.0', color=colores[1], fontsize=10, transform=vpp_legend_ax.transAxes),
    vpp_legend_ax.text(0.05, 0.35, f'CH3: Vpp=0.0', color=colores[2], fontsize=10, transform=vpp_legend_ax.transAxes),
    vpp_legend_ax.text(0.05, 0.15, f'CH4: Vpp=0.0', color=colores[3], fontsize=10, transform=vpp_legend_ax.transAxes)
]
#____________________________________________________________________________________________________________________________________________
# Funciones de botones
def toggle_pause(event):
    global pausado
    pausado = not pausado
    btn_pause.label.set_text('Reanudar' if pausado else 'Pausa')

def toggle_save(event):
    global guardar_datos, datos_guardados
    guardar_datos = not guardar_datos
    if not guardar_datos and datos_guardados:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f'osciloscopio_datos_{timestamp}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'CH0', 'CH1', 'CH2', 'CH3'])
            writer.writerows(datos_guardados)
        datos_guardados = []
    btn_save.label.set_text('Detener' if guardar_datos else 'Guardar')

def toggle_ch0(event):
    canales_activos[0] = not canales_activos[0]
    linea_ch0.set_visible(canales_activos[0])
    btn_ch0.color = (0.05, 0.05, 0.15, 0.7) if canales_activos[0] else (0.3, 0.1, 0.1, 0.7)

def toggle_ch1(event):
    canales_activos[1] = not canales_activos[1]
    linea_ch1.set_visible(canales_activos[1])
    btn_ch1.color = (0.05, 0.05, 0.15, 0.7) if canales_activos[1] else (0.3, 0.1, 0.1, 0.7)

def toggle_ch2(event):
    canales_activos[2] = not canales_activos[2]
    linea_ch2.set_visible(canales_activos[2])
    btn_ch2.color = (0.05, 0.05, 0.15, 0.7) if canales_activos[2] else (0.3, 0.1, 0.1, 0.7)

def toggle_ch3(event):
    canales_activos[3] = not canales_activos[3]
    linea_ch3.set_visible(canales_activos[3])
    btn_ch3.color = (0.05, 0.05, 0.15, 0.7) if canales_activos[3] else (0.3, 0.1, 0.1, 0.7)

def reset_data(event):
    with buffer_lock:
        valores_ch0.clear()
        valores_ch1.clear()
        valores_ch2.clear()
        valores_ch3.clear()
        valores_ch0.extend([0] * BUFFER_SIZE)
        valores_ch1.extend([0] * BUFFER_SIZE)
        valores_ch2.extend([0] * BUFFER_SIZE)
        valores_ch3.extend([0] * BUFFER_SIZE)
#____________________________________________________________________________________________________________________________________________
# Conectr botones
btn_pause.on_clicked(toggle_pause)
btn_save.on_clicked(toggle_save)
btn_ch0.on_clicked(toggle_ch0)
btn_ch1.on_clicked(toggle_ch1)
btn_ch2.on_clicked(toggle_ch2)
btn_ch3.on_clicked(toggle_ch3)
btn_reset.on_clicked(reset_data)

def update_scale(val):
    ax_main.set_ylim(0, slider_scale.val)

slider_scale.on_changed(update_scale)
#____________________________________________________________________________________________________________________________________________
# Función para actualizar el gráfico
def actualizar(frame):
    with buffer_lock:
        # Actualizar datos de las líneas
        datos = [
            np.array(valores_ch0) if canales_activos[0] else np.zeros(BUFFER_SIZE),
            np.array(valores_ch1) if canales_activos[1] else np.zeros(BUFFER_SIZE),
            np.array(valores_ch2) if canales_activos[2] else np.zeros(BUFFER_SIZE),
            np.array(valores_ch3) if canales_activos[3] else np.zeros(BUFFER_SIZE)
        ]
        
        linea_ch0.set_ydata(datos[0])
        linea_ch1.set_ydata(datos[1])
        linea_ch2.set_ydata(datos[2])
        linea_ch3.set_ydata(datos[3])
        
        # Actualizar displays digitales
        valores_actuales = [
            valores_ch0[-1] if canales_activos[0] and len(valores_ch0) > 0 else 0,
            valores_ch1[-1] if canales_activos[1] and len(valores_ch1) > 0 else 0,
            valores_ch2[-1] if canales_activos[2] and len(valores_ch2) > 0 else 0,
            valores_ch3[-1] if canales_activos[3] and len(valores_ch3) > 0 else 0
        ]
        
        for i, (text, valor) in enumerate(zip(display_texts, valores_actuales)):
            if canales_activos[i]:
                text.set_text(f'{valor:04d}')
                text.set_color('white')
            else:
                text.set_text('----')
                text.set_color('gray')
        
        # Actualizar Vpp en la leyenda
        for i, (text, datos) in enumerate(zip(vpp_texts, [valores_ch0, valores_ch1, valores_ch2, valores_ch3])):
            if canales_activos[i] and len(datos) > 0:
                peak_to_peak = np.max(datos) - np.min(datos)
                text.set_text(f'CH{i+1}: Vpp={peak_to_peak:.1f}')
            else:
                text.set_text(f'CH{i+1}: Vpp=0.0')
    
    return [linea for i, linea in enumerate([linea_ch0, linea_ch1, linea_ch2, linea_ch3]) if canales_activos[i]] + display_texts + vpp_texts
#____________________________________________________________________________________________________________________________________________
# Animación en tiempo real
ani = animation.FuncAnimation(fig, actualizar, interval=10, cache_frame_data=False, blit=True)
plt.tight_layout()
plt.show()