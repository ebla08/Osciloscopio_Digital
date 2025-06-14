#include <SPI.h>

const int CS_PIN = 10;  // Chip Select conectado al pin 10

void setup() {
  SPI.begin();
  pinMode(CS_PIN, OUTPUT);
  digitalWrite(CS_PIN, HIGH);
  Serial.begin(115200);
}

int leerMCP3208(byte canal) {
  byte comando = 0b00000110 | ((canal & 0x04) >> 2); 
  byte segundo = (canal & 0x03) << 6;                

  digitalWrite(CS_PIN, LOW);
  SPI.transfer(comando);
  int alta = SPI.transfer(segundo) & 0x0F;           
  int baja = SPI.transfer(0x00);
  digitalWrite(CS_PIN, HIGH);

  return (alta << 8) | baja;  // Resultado de 12 bits
}

void loop() {
  int valor0 = leerMCP3208(0);  // CH0
  int valor1 = leerMCP3208(1);  // CH1
  int valor2 = leerMCP3208(2);  // CH2
  int valor3 = leerMCP3208(3);  // CH3

  // Enviar los 4 canales separados por comas
  Serial.print(valor0);
  Serial.print(",");
  Serial.print(valor1);
  Serial.print(",");
  Serial.print(valor2);
  Serial.print(",");
  Serial.println(valor3);

  delay(25);  
}