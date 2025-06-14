Osciloscopio Digital de 4 Canales
Un osciloscopio digital de 4 canales de bajo costo y código abierto, construido con Arduino y Python.
Descripción General
Este proyecto presenta un osciloscopio digital de 4 canales diseñado para la adquisición y visualización en tiempo real de señales analógicas. Utiliza hardware de código abierto (Arduino con ADC MCP3208) y software (Python con Matplotlib) para ofrecer una alternativa económica a los osciloscopios comerciales.
Objetivos

General: Desarrollar un sistema de código abierto para adquirir y visualizar señales analógicas de 4 canales.
Específicos:
Implementar adquisición de datos con ADC de 12 bits.
Crear una interfaz gráfica de usuario en tiempo real.
Habilitar funciones de control y almacenamiento de datos.
Calcular parámetros de señal como voltaje pico a pico (Vpp).



Arquitectura del Sistema
Hardware

Plataforma: Arduino con ADC MCP3208 de 12 bits (8 canales, 4 utilizados).
Especificaciones del MCP3208:
Resolución: 12 bits (4096 niveles)
Comunicación: SPI
Frecuencia de muestreo: Hasta 100 ksps (el sistema opera a ~40 Hz)


Funcionamiento:
Arduino inicializa la comunicación SPI con el MCP3208.
Lee secuencialmente los 4 canales analógicos.
Transmite datos de 12 bits (0-4095) por puerto serie en formato CSV.



Software

Lenguaje: Python
Librerías Principales:
matplotlib: Visualización de formas de onda en tiempo real
serial: Comunicación por puerto serie
threading: Procesamiento paralelo
numpy: Operaciones matemáticas
collections: Estructuras de datos eficientes


Configuración:PUERTO = 'COM3'  # Ajustar según el sistema
VELOCIDAD = 115200  # Velocidad de baudios
BUFFER_SIZE = 200  # Muestras por canal


Almacenamiento de Datos: Buffers circulares (collections.deque) para cada canal.

Características
Adquisición de Datos

Lee datos seriales en formato CSV (4 valores por línea).
Valida y almacena datos en buffers circulares con protección thread-safe.
Permite exportar datos a CSV con marcas de tiempo.

Visualización en Tiempo Real

Componentes de la Interfaz:
Gráfico de formas de onda de 4 canales.
Lecturas digitales de valores instantáneos por canal.
Panel de voltaje pico a pico (Vpp).
Controles para pausa, guardado, activación de canales y reinicio.


Controles:
Pausa/Reanudar: Detiene/reanuda la adquisición de datos.
Guardar: Exporta datos a CSV.
Activar/Desactivar Canales: Habilita/desactiva la visualización de cada canal.
Escala Y: Ajusta el rango vertical (100-4095).


Mediciones:
Cálculo de Vpp en tiempo real.
Registro de datos con marcas de tiempo.



Especificaciones Técnicas

Resolución ADC: 12 bits (4096 niveles)
Canales: 4 simultáneos
Tamaño de Buffer: 200 muestras por canal
Frecuencia de Actualización Gráfica: 100 Hz (intervalo de 10 ms)
Comunicación: UART (115200 baudios, formato CSV)
Resolución de la Interfaz: Recomendada 1600x1000 píxeles
Tema: Modo oscuro con colores diferenciados por canal

Ventajas

Bajo costo en comparación con osciloscopios comerciales.
Código abierto y personalizable.
Soporta 4 canales simultáneos.
Interfaz gráfica intuitiva con mediciones automáticas.
Exportación de datos para análisis posterior.

Limitaciones

Frecuencia de muestreo limitada (~40 Hz).
Baja resolución temporal.
Dependencia de la estabilidad del puerto serie.
Rango de voltaje limitado por el ADC.

Mejoras Futuras

Implementar disparo automático (trigger).
Añadir análisis de frecuencia (FFT).
Incluir cursores de medición.
Aumentar la frecuencia de muestreo.
Habilitar calibración automática.
Soporte para operaciones matemáticas entre canales.
Desarrollar una interfaz web para acceso remoto.

Conclusiones
El osciloscopio cumple con los objetivos establecidos, proporcionando una solución funcional y económica para la visualización de señales analógicas. Aunque es estable, hay espacio para mejoras en rendimiento y calidad de la interfaz. Frameworks como PyQt5, PyQt6 o Tkinter podrían optimizar la interfaz, pero requieren más tiempo de aprendizaje.
Instrucciones de Instalación

Hardware:
Conecta el MCP3208 al Arduino mediante SPI.
Conecta las entradas analógicas a los canales deseados.


Software:pip install matplotlib pyserial numpy


Actualiza PUERTO en el script de Python según tu puerto serie.
Ejecuta el script de Python para iniciar la interfaz gráfica.


Código Arduino:
Carga el sketch proporcionado en el Arduino para configurar el MCP3208 y la salida serial.



Estructura del Repositorio
├── arduino/
│   └── osciloscopio.ino
├── python/
│   └── osciloscopio.py
├── README.md
└── LICENSE

Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
