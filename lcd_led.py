import time
import board
import digitalio
import adafruit_dht
import I2C_LCD_driver

rote_led = digitalio.DigitalInOut(board.D21)
rote_led.direction = digitalio.Direction.OUTPUT

dhtDevice = adafruit_dht.DHT11(board.D4)
lcd = I2C_LCD_driver.lcd()

while True:
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        if humidity is not None:
            temperature_f = temperature_c * (9 / 5) + 32

            if temperature < 20:
                rote_led.value = True
            else:
                rote_led.value = False

            print(f"Temp: {temperature_c:.1f}°C / {temperature_f:.1f}°F | Humidity: {humidity}%")

            lcd.lcd_display_string("Temp: {:.0f}F ({:.0f}C)   ".format(temperature_f, temperature_c), 1)
            lcd.lcd_display_string("Humidity: {:.0f}%   ".format(humidity), 2)

    except RuntimeError as error:
        print(f"Lesefehler: {error.args[0]}")
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        rote_led.deinit()
        raise error

    time.sleep(2.0)
