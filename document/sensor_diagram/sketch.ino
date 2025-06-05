//definicao dos pinos

const int POT_PIN = 34;
const int LED_VERDE = 27;
const int LED_AMARELO = 26;
const int LED_VERMELHO = 25;

//pressao hidrostatica 
const float PRESSAO_MIN_KPA = 180;
const float PRESSAO_MAX_KPA = 700;

//limiares de alerta
const float LIMITE_OK_KPA = 400;
const float LIMITE_ATENCAO_KPA = 550;

void setup() {

  Serial.begin(115200);
  //Serial.println("Hello, ESP32!");
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARELO, OUTPUT);
  pinMode(LED_VERMELHO, OUTPUT);

//inicializar leds desligados
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AMARELO, LOW);
  digitalWrite(LED_VERMELHO, LOW);

}

void loop() {
//ler o potenciometro
  int potValue = analogRead(POT_PIN);
//mapear escalas
 
  float pressao_simulada_kpa = map(potValue, 0, 4095, (int) (PRESSAO_MIN_KPA * 100), (int)(PRESSAO_MAX_KPA * 100)) / 100.0;
//garantir pressao nao negativa
 if (pressao_simulada_kpa < 0) {
  pressao_simulada_kpa = 0;
 }
  
//logica de acionamento dos leds e impressao
Serial.print("Pressao Simulada: ");
Serial.print(pressao_simulada_kpa, 2); // 2 casas decimais
Serial.print(" kPa | Status: ");

//logica dos leds
if (pressao_simulada_kpa < LIMITE_OK_KPA) {
    digitalWrite(LED_VERDE, HIGH);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, LOW);
    Serial.println("OK (Verde)");
  } else if (pressao_simulada_kpa < LIMITE_ATENCAO_KPA) {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, HIGH);
    digitalWrite(LED_VERMELHO, LOW);
    Serial.println("ATENÇÃO (Amarelo)");
  } else {
    digitalWrite(LED_VERDE, LOW);
    digitalWrite(LED_AMARELO, LOW);
    digitalWrite(LED_VERMELHO, HIGH);
    Serial.println("EMERGÊNCIA (Vermelho)!");
  }

  delay(500);

}

