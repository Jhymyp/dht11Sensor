# Raspberry Pi 3 Umweltdaten- & Überwachungssystem

Ein automatisierte System zur Umweltüberwachung für den Raspberry Pi 3. Das Projekt liest Umgebungstemperatur und relative Luftfeuchtigkeit über einen DHT11-Sensor aus, zeigt die Echtzeitdaten auf einem 16x2 I2C-LCD-Display an und steuert eine rote Warn-LED an, sobald die relative Luftfeuchtigkeit 50 % überschreitet.

## Funktionen

* **Echtzeit-Telemetrie**: Messung von Umgebungstemperatur (°C und °F) sowie relativer Luftfeuchtigkeit (%).
* **I2C-LCD-Anzeige**: Die Messwerte werden alle 2 Sekunden auf einem 16x2 Zeichen LCD-Display aktualisiert.
* **Visueller Alarm**: Automatischer Luftfeuchtigkeits-Alarm schaltet GPIO 21 ein, um eine rote LED zu aktivieren, wenn die Luftfeuchtigkeit über 50 % steigt.
* **Moderne Hardware-Abstraktion**: Verwendet `adafruit-blinka` und `libgpiod` für die Ansteuerung unter aktuellen Linux-Kerneln.
* **Fehlertoleranz**: Fängt vorübergehende Sensor-Lese-Fehler ab, um Script-Abstürze zu verhindern.

## Stückliste (Hardware-Anforderungen)

1. **Raspberry Pi 3** (mit Raspberry Pi OS)
2. **DHT11 Temperatur- und Luftfeuchtigkeitssensor**
3. **16x2 LCD-Display mit PCF8574 I2C-Backpack**
4. **Rote LED** & **220Ω - 470Ω Widerstand** (Vorwiderstand zur Strombegrenzung)
5. **4,7kΩ - 10kΩ Widerstand** (Pull-up-Widerstand für die DHT11-Datenleitung, falls ein einzelner 4-Pin-Sensor verwendet wird)
6. **Steckbrett (Breadboard) und Jumper-Kabel**

## Schaltplan & Pin-Belegung

### Pinout-Tabelle

| Komponente | Pin-Funktion | Zielanschluss | BCM-Pin / Board-Mapping | Physischer Header-Pin | 
| ----- | ----- | ----- | ----- | ----- | 
| **DHT11 Sensor** | VCC | 3,3V Stromversorgung | 3.3V | Pin 1 | 
|  | DATA | Digitaler Signaleingang | BCM 4 (`board.D4`) | Pin 7 | 
|  | GND | Masse (Ground) | GND | Pin 6 | 
| **Rote LED** | Anode (+) | Digitaler Signalausgang | BCM 21 (`board.D21`) | Pin 40 | 
|  | Kathode (-) | Masse (über Widerstand) | GND | Pin 39 | 
| **I2C LCD Backpack** | VCC | 5V Stromversorgung | 5V | Pin 2 | 
|  | GND | Masse (Ground) | GND | Pin 9 | 
|  | SDA | Serielles Datensignal | BCM 2 (SDA) | Pin 3 | 
|  | SCL | Serielles Taktsignal | BCM 3 (SCL) | Pin 5 | 

*Hinweis: Wenn Sie einen Standalone-DHT11-Sensor mit 4 Pins verwenden, schalten Sie einen 4,7kΩ–10kΩ Pull-up-Widerstand zwischen die DATA-Leitung und die 3,3V VCC-Stromversorgung.*

## Systemanforderungen & Software-Einrichtung

Führen Sie diese Schritte auf Ihrem Raspberry Pi 3 aus, um das Betriebssystem zu konfigurieren und alle Software-Abhängigkeiten zu installieren.

### Schritt 1: Installation der Systempakete

Aktualisieren Sie die Paketlisten und installieren Sie die erforderlichen Linux-Utilities, GPIO-Bibliotheken und Python-Pakete:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-dev python3-venv i2c-tools python3-smbus libgpiod2
```

### Schritt 2: Konfiguration der Hardware-Schnittstellen

Aktivieren Sie die Hardware-I2C-Schnittstelle:

```bash
sudo raspi-config nonint do_i2c 0
```

Überprüfen Sie, ob das I2C-LCD-Backpack auf Bus 1 erkannt wird (meistens unter der Adresse `0x27` oder `0x3f`):

```bash
i2cdetect -y 1
```

Fügen Sie Ihren Benutzer zu den entsprechenden Hardware-Zugriffsgruppen hinzu:

```bash
sudo usermod -aG gpio,i2c $USER
```

*(Bitte melden Sie sich ab und wieder an, damit die Gruppenberechtigungen wirksam werden).*

### Schritt 3: Einrichten einer virtuellen Python-Umgebung

Klonen Sie Ihr Repository und erstellen Sie eine isolierte virtuelle Python-Umgebung:

```bash
git clone https://github.com/Jhymyp/dht11Sensor/

python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

### Schritt 4: Installation der Python-Pakete

Aktualisieren Sie die zentralen Python-Tools und installieren Sie die Adafruit CircuitPython-Pakete:

```bash
pip3 install --upgrade pip setuptools wheel
pip3 install adafruit-blinka adafruit-circuitpython-dht
```

## Datei-Übersicht

* **`lcd_led.py`**: Hauptskript, das den DHT11-Sensor abfragt, das I2C-LCD-Display aktualisiert und die Warn-LED steuert.
* **`I2C_LCD_driver.py`**: I2C-Treiberbibliothek zur Kommunikation mit dem PCF8574 LCD-Display-Modul.
* **`README.md`**: Technische Übersicht und Installationsanleitung.

## Ausführen der Anwendung

1. Aktivieren Sie die virtuelle Umgebung:

   ```bash
   source .venv/bin/activate
   ```

2. Starten Sie das Überwachungsprogramm:

   ```bash
   python3 lcd_led.py
   ```

### Übersicht der Ausgaben

* **Konsolen-Ausgabe**: Zeigt den Messwert im Terminal an, z. B. `Temp: 23.5°C / 74.3°F | Humidity: 54%`.
* **LCD-Anzeige**:
  * Zeile 1: `Temp: 74F (24C)`
  * Zeile 2: `Humidity: 54%`
* **Visueller Alarm**: Die LED schaltet sich EIN, wenn die Luftfeuchtigkeit 50 % überschreitet, und wieder AUS, wenn sie bei oder unter 50 % liegt.

## Fehlerbehebung (Troubleshooting)

| Problem / Fehler | Ursache | Lösung | 
| ----- | ----- | ----- | 
| `Timed out waiting for PulseIn message` | `libgpiod2`-Treiber fehlt oder ein Prozesskonflikt liegt vor. | Treiber neu installieren über `sudo apt install --reinstall libgpiod2`. | 
| `PermissionError: [Errno 13] Permission denied` | Benutzer ist nicht in den benötigten Hardware-Gruppen. | Führen Sie `sudo usermod -aG i2c,gpio $USER` aus und melden Sie sich neu an. | 
| Display-Hintergrundbeleuchtung ist AN, aber kein Text sichtbar | Kontrast-Potenziometer ist falsch eingestellt oder falsche I2C-Adresse. | Rufen Sie `i2cdetect -y 1` auf, um die Adresse zu prüfen, und stellen Sie das blaue Potenziometer auf der Rückseite des LCDs ein. | 
| `ImportError: No module named 'adafruit_dht'` | Das Skript wird außerhalb der virtuellen Umgebung ausgeführt. | Aktivieren Sie die Umgebung vor dem Start mit `source .venv/bin/activate`. | 
