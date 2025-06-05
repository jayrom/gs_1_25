// ID do sensor
const int sensorId = 1;

// Definição dos pinos

const int POT_PIN = 34;
const int LED_VERDE = 27;
const int LED_AMARELO = 26;
const int LED_VERMELHO = 25;

// Pressão hidrostática 
const float PRESSAO_MIN_KPA = 180;
const float PRESSAO_MAX_KPA = 700;

// Limiares de alerta
const float LIMITE_OK_KPA = 400;
const float LIMITE_ATENCAO_KPA = 550;

void setup() {
  Serial.begin(115200);
   
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);

// Inicializar leds desligados
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AMARELO, LOW);
  digitalWrite(LED_VERMELHO, LOW);

// Cabeçalho do CSV
Serial.println("sensor,time,pressao,cor_do_led,");

}

void loop() {

// ID do sensor
  Serial.print(sensorId);
  Serial.print(",");

// Timestamp
  Serial.print(millis());
  Serial.print(",");

// Ler o potenciômetro
  int potValue = analogRead(POT_PIN);

// Mapear escalas
  float pressao_simulada_kpa = map(potValue, 0, 4095, (int) (PRESSAO_MIN_KPA * 100), (int)(PRESSAO_MAX_KPA * 100)) / 100.0;

// Garantir pressao nao negativa
  if (pressao_simulada_kpa < 0) {
    pressao_simulada_kpa = 0;
  }
  
// Lógica de acionamento dos leds e impressão

Serial.print(pressao_simulada_kpa, 2);
Serial.print(",");

// Lógica dos leds
if (pressao_simulada_kpa < LIMITE_OK_KPA) {
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, LOW);
    Serial.print("Verde");
    Serial.println(",");
  } else if (pressao_simulada_kpa < LIMITE_ATENCAO_KPA) {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, HIGH);
    digitalWrite(LED_VERMELHO, LOW);
    Serial.print("Amarelo");
    Serial.println(",");
  } else {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, HIGH);
    Serial.print("Vermelho");
    Serial.println(",");
  }

  delay(1000);
}


