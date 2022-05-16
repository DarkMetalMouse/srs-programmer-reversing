// the setup function runs once when you press reset or power the board
void setup()
{
  Serial.begin(77170);
  Serial1.begin(77170);
}

// the loop function runs over and over again forever
void loop()
{
  while (Serial.available())
  {
    Serial1.write(Serial.read());
  }
  while (Serial1.available())
  {
    Serial.write(Serial1.read());
  }
}
