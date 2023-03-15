# Serial Projector

A simple Chrome Application that shows last line of text got from serial port with a big font.

[Google Chrome extension](https://github.com/amperka/serial-projector)

# Installation

You can install last version on [Git Hub](https://github.com/Grigoriy457/python-serial-projector/releases).

# Usage

Just send text to serial. Once Serial Projector will see end of line (`\n`)
the text on sceen will be updated.

You can send UTF-8 unicode and HTML.

```cpp
void setup()
{
  Serial.begin(9600);
}
void loop()
{
  int t = analogRead(A0) / 100;
  Serial.print("<div style='font-size: 0.2em'>Температура / Temperature</div>");
  Serial.print(t);
  Serial.println(" ℃");
}
```

Use buttons at the bottom right corner to adjust application settings.

# Authors
Written by Grigoriy Vlasov.
