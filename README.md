# Osciloscopio Digital de 4 Canales
## Arduino + Python

---

## Introducción
![image](https://github.com/user-attachments/assets/20a757b4-1c8d-4076-bc7a-b03de4f70a86)

El presente informe describe el diseño, implementación y funcionamiento de un osciloscopio digital de 4 canales desarrollado mediante la integración de hardware Arduino y software Python.

---

## Objetivos
### Objetivo General
Desarrollar un sistema de adquisición de datos y visualización de señales analógicas de 4 canales utilizando tecnologías de código abierto.
### Objetivos Específicos

- Implementar la adquisición de datos analógicos mediante ADC de 12 bits
- Desarrollar interfaz gráfica de usuario en tiempo real  
- Proporcionar funciones de control y almacenamiento de datos
- Calcular parámetros de señal como voltaje pico a pico (Vpp)

---

## Marco Teórico

Un osciloscopio digital es un instrumento de medición electrónica que permite visualizar señales eléctricas variantes en el tiempo. A diferencia de los osciloscopios analógicos tradicionales, los digitales convierten las señales analógicas en datos digitales para su procesamiento y visualización.

### Componentes Principales

- Sistema de Adquisición: Convierte señales analógicas a digitales
- Procesamiento: Manipula y almacena los datos digitalizados  
- Visualización: Presenta las formas de onda en pantalla
- Control: Permite ajustar parámetros de medición

---

## Arquitectura del Sistema

### Hardware - Arduino

El subsistema de hardware está basado en Arduino y utiliza el conversor analógico-digital MCP3208 de 12 bits con 8 canales.

#### Especificaciones del MCP3208

- Resolución: 12 bits (4096 niveles)
- Canales: 8 (utilizamos 4)
- Comunicación: SPI
- Velocidad de muestreo: Hasta 100 ksps

#### Funcionamiento del Hardware

1. El Arduino inicializa la comunicación SPI con el MCP3208
2. En bucle continuo, lee secuencialmente los 4 canales analógicos
3. Cada lectura retorna un valor de 12 bits (0-4095)
4. Los datos se transmiten por puerto serie en formato CSV
5. La frecuencia de muestreo es aproximadamente 40 Hz

### Software - Aplicación Python

El software de visualización está desarrollado en Python utilizando las siguientes librerías:

#### Librerías Principales

- matplotlib: Visualización gráfica y animación
- serial: Comunicación puerto serie
- threading: Procesamiento paralelo
- numpy: Operaciones matemáticas
- collections: Estructuras de datos eficientes

#### Arquitectura del Software

```python
# Configuración del sistema
PUERTO = 'COM3'  # Depende que puerto COM se esté usando, puede variar
VELOCIDAD = 115200
BUFFER_SIZE = 200

# Buffers circulares para cada canal
valores_ch0 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
valores_ch1 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
valores_ch2 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
valores_ch3 = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
```

---

## Funcionamiento del Sistema

### Adquisición de Datos

#### Proceso

1. Lee continuamente líneas del puerto serie
2. Parsea los datos CSV (4 valores separados por comas)
3. Valida que sean números enteros
4. Almacena en buffers circulares con protección thread-safe
5. Opcionalmente guarda datos para exportación

### Visualización en Tiempo Real

#### Interfaz Gráfica
- **Panel Principal:** Gráfico de formas de onda de 4 canales
- **Displays Digitales:** Valores numéricos actuales de cada canal
- **Panel Vpp:** Voltaje pico a pico calculado
- **Controles:** Botones para pausa, guardado, activación de canales

#### Características Funcionales

Controles Disponibles:

- **Pausa/Reanudar:** Detiene/reanuda la adquisición de datos
- **Guardar:** Exporta datos a archivo CSV con timestamp
- **CH1-CH4:** Activa/desactiva visualización de cada canal
- **Reiniciar:** Limpia todos los buffers de datos
- **Escala Y:** Ajusta rango vertical del gráfico (100-4095)

Mediciones Automáticas:

- Valor instantáneo digital para cada canal
- Voltaje pico a pico (Vpp) calculado en tiempo real
- Timestamp para datos guardados

---

## Especificaciones Técnicas

### Rendimiento del Sistema

- **Resolución ADC:** 12 bits (4096 niveles)
- **Canales simultáneos:** 4
- **Tamaño de buffer:** 200 muestras por canal
- **Frecuencia de actualización gráfica:** 100 Hz (intervalo 10ms)

### Comunicación

- **Protocolo:** UART (Serial)
- **Velocidad:** 115200 baudios
- **Formato:** CSV (valor1, valor2, valor3, valor4)

### Interfaz de Usuario
- **Resolución recomendada:** 1600x1000 píxeles
- **Colores diferenciados por canal**
- **Tema oscuro para mejor visibilidad**
- **Controles intuitivos con retroalimentación visual**

---

## Ventajas y Limitaciones

### Ventajas
- Bajo costo comparado con osciloscopios comerciales
- Código abierto y modificable
- 4 canales simultáneos
- Exportación de datos para análisis posterior
- Interfaz gráfica intuitiva
- Cálculos automáticos (Vpp)

### Limitaciones
- Frecuencia de muestreo limitada
- Resolución temporal baja
- Dependiente de la estabilidad del puerto serie
- Rango de voltaje limitado por el ADC

---

## Trabajo Futuro

### Mejoras Propuestas
1. Implementación de trigger automático
2. Análisis de frecuencia (FFT)
3. Cursores de medición
4. Mayor frecuencia de muestreo
5. Calibración automática
6. Funciones matemáticas entre canales
7. Interfaz web para acceso remoto

---

## Conclusiones

El sistema desarrollado cumple exitosamente con los objetivos planteados, proporcionando una solución funcional y económica para la visualización de señales analógicas.

Si bien el proyecto está sujeto a mejoras tanto visuales como funcionales, funciona de manera "estable".

Se podría haber creado una interfaz de mucha más calidad usando PyQt5, PyQt6 o Tkinter junto a un archivo ejecutable (como un programa más en el ordenador) y demás, pero en lo personal requiere una curva de aprendizaje que requiere un poco más de tiempo.

---

## Instalación y Uso

### Requisitos
- Arduino Uno/Nano
- MCP3208 ADC
- Python 3.x
- Librerías: `matplotlib`, `pyserial`, `numpy`

### Instalación de dependencias
```bash
pip install matplotlib pyserial numpy
```

### Ejecución
1. Conectar el hardware Arduino con MCP3208
2. Subir el código Arduino correspondiente
3. Ejecutar la aplicación Python
4. Configurar el puerto serie correcto en el código
