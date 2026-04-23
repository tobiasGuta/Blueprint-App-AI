"""
Component Database — The source of truth for all selectable electronics parts.
Each component has: name, category, description, 3D dimensions (cm), color, and pin list.
"""

COMPONENT_DATABASE = {
    # ─── MICROCONTROLLERS ─────────────────────────────────────────────────────
    "arduino_uno": {
        "name": "Arduino Uno R3",
        "category": "microcontroller",
        "description": "ATmega328P, 14 digital I/O, 6 analog inputs, 16 MHz, 5V logic",
        "dimensions": {"w": 6.8, "h": 0.6, "d": 5.3},
        "color": "#1a6bcc",
        "pins": ["5V", "3.3V", "GND", "GND2", "VIN", "D0_RX", "D1_TX", "D2", "D3_PWM",
                 "D4", "D5_PWM", "D6_PWM", "D7", "D8", "D9_PWM", "D10_SS", "D11_MOSI",
                 "D12_MISO", "D13_SCK", "A0", "A1", "A2", "A3", "A4_SDA", "A5_SCL",
                 "RESET", "AREF"]
    },
    "esp32_devkit": {
        "name": "ESP32 DevKit V1",
        "category": "microcontroller",
        "description": "Dual-core 240 MHz, WiFi + BT 4.2, 4 MB Flash, 38 GPIO pins",
        "dimensions": {"w": 5.5, "h": 0.5, "d": 2.8},
        "color": "#1a6bcc",
        "pins": ["3V3", "GND", "EN", "GPIO0", "GPIO2", "GPIO4", "GPIO5", "GPIO12",
                 "GPIO13", "GPIO14", "GPIO15", "GPIO16", "GPIO17", "GPIO18", "GPIO19",
                 "GPIO21_SDA", "GPIO22_SCL", "GPIO23_MOSI", "GPIO25", "GPIO26", "GPIO27",
                 "GPIO32", "GPIO33", "GPIO34", "GPIO35", "GPIO36", "GPIO39", "VIN"]
    },
    "raspberry_pi_pico": {
        "name": "Raspberry Pi Pico",
        "category": "microcontroller",
        "description": "RP2040 dual-core ARM M0+ @ 133 MHz, 264 KB SRAM, 2 MB Flash",
        "dimensions": {"w": 5.1, "h": 0.3, "d": 2.1},
        "color": "#006633",
        "pins": ["GP0_TX", "GP1_RX", "GND", "GP2", "GP3", "GP4_SDA", "GP5_SCL",
                 "GP6", "GP7", "GP8", "GP9", "GP10", "GP11", "GP12", "GP13",
                 "GP14", "GP15", "GP16_MISO", "GP17_CS", "GP18_SCK", "GP19_MOSI",
                 "GP20", "GP21", "GP22", "GP26_A0", "GP27_A1", "GP28_A2",
                 "3V3", "VSYS", "VBUS"]
    },
    "flight_controller_f4": {
        "name": "F4 Flight Controller",
        "category": "microcontroller",
        "description": "STM32F405 @ 168 MHz, MPU6000 IMU, Betaflight, 4-motor outputs",
        "dimensions": {"w": 3.6, "h": 0.5, "d": 3.6},
        "color": "#003388",
        "pins": ["5V", "GND", "MOTOR1", "MOTOR2", "MOTOR3", "MOTOR4",
                 "UART1_TX", "UART1_RX", "UART2_TX", "UART2_RX",
                 "SDA", "SCL", "LED", "BUZZER", "VBAT", "CURR", "RSSI"]
    },
    "raspberry_pi_4b": {
        "name": "Raspberry Pi 4 Model B",
        "category": "microcontroller",
        "description": "Quad-core Cortex-A72 @ 1.8 GHz, 4 GB RAM, WiFi, BT5, USB3",
        "dimensions": {"w": 8.5, "h": 1.7, "d": 5.6},
        "color": "#cc0033",
        "pins": ["5V_1", "5V_2", "3V3_1", "3V3_2", "GND_1", "GND_2", "GPIO2_SDA",
                 "GPIO3_SCL", "GPIO4", "GPIO5", "GPIO6", "GPIO7", "GPIO8_CE0",
                 "GPIO9_MISO", "GPIO10_MOSI", "GPIO11_CLK", "GPIO12_PWM0",
                 "GPIO13_PWM1", "GPIO14_TXD", "GPIO15_RXD", "GPIO17", "GPIO18",
                 "GPIO22", "GPIO23", "GPIO24", "GPIO25", "GPIO26", "GPIO27"]
    },

    # ─── SENSORS ──────────────────────────────────────────────────────────────
    "dht22": {
        "name": "DHT22 Temp & Humidity",
        "category": "sensor",
        "description": "Digital sensor: -40–80 °C ±0.5 °C, 0–100 % RH ±2 %, single-wire",
        "dimensions": {"w": 1.5, "h": 3.5, "d": 1.0},
        "color": "#008855",
        "pins": ["VCC", "DATA", "NC", "GND"]
    },
    "mpu6050": {
        "name": "MPU-6050 IMU",
        "category": "sensor",
        "description": "3-axis gyro + 3-axis accel, I2C/SPI, built-in DMP, ±250–2000 °/s",
        "dimensions": {"w": 2.0, "h": 0.3, "d": 1.6},
        "color": "#008855",
        "pins": ["VCC", "GND", "SCL", "SDA", "XDA", "XCL", "AD0", "INT"]
    },
    "hc_sr04": {
        "name": "HC-SR04 Ultrasonic",
        "category": "sensor",
        "description": "Ultrasonic distance sensor, 2–400 cm, ±3 mm accuracy, 5V",
        "dimensions": {"w": 4.5, "h": 2.0, "d": 1.7},
        "color": "#008855",
        "pins": ["VCC", "TRIG", "ECHO", "GND"]
    },
    "bmp280": {
        "name": "BMP280 Pressure",
        "category": "sensor",
        "description": "Barometric pressure + temperature, I2C/SPI, ±1 hPa, 300–1100 hPa",
        "dimensions": {"w": 1.1, "h": 0.2, "d": 1.1},
        "color": "#008855",
        "pins": ["VCC", "GND", "SCL", "SDA", "CSB", "SDO"]
    },
    "soil_moisture_sensor": {
        "name": "Capacitive Soil Sensor",
        "category": "sensor",
        "description": "Corrosion-resistant capacitive soil moisture sensor, 3.3–5.5 V, analog out",
        "dimensions": {"w": 3.0, "h": 0.3, "d": 1.0},
        "color": "#008855",
        "pins": ["VCC", "GND", "AOUT"]
    },
    "pir_hcsr501": {
        "name": "HC-SR501 PIR Sensor",
        "category": "sensor",
        "description": "Passive IR motion detector, 3–7 m range, adjustable sensitivity & delay",
        "dimensions": {"w": 3.2, "h": 5.0, "d": 2.4},
        "color": "#008855",
        "pins": ["VCC", "OUT", "GND"]
    },
    "neo_6m_gps": {
        "name": "NEO-6M GPS",
        "category": "sensor",
        "description": "u-blox NEO-6M, UART, 1–5 Hz update, built-in 25 × 25 mm patch antenna",
        "dimensions": {"w": 2.5, "h": 0.4, "d": 3.5},
        "color": "#008855",
        "pins": ["VCC", "GND", "TXD", "RXD", "PPS"]
    },
    "ph_sensor": {
        "name": "pH Sensor Module",
        "category": "sensor",
        "description": "Analog pH probe interface, 0–14 pH range, BNC connector, 5 V",
        "dimensions": {"w": 4.2, "h": 1.5, "d": 3.2},
        "color": "#008855",
        "pins": ["VCC", "GND", "PO", "DO"]
    },
    "water_level_sensor": {
        "name": "Water Level Sensor",
        "category": "sensor",
        "description": "Resistive water level probe, 5 V, analog + digital output",
        "dimensions": {"w": 6.2, "h": 0.3, "d": 1.6},
        "color": "#008855",
        "pins": ["VCC", "GND", "SIGNAL"]
    },
    "lm35_temp": {
        "name": "LM35 Temperature Sensor",
        "category": "sensor",
        "description": "Precision analog temp sensor, −55–150 °C, 10 mV/°C, TO-92",
        "dimensions": {"w": 0.5, "h": 1.3, "d": 0.5},
        "color": "#008855",
        "pins": ["VCC", "VOUT", "GND"]
    },

    # ─── ACTUATORS / MOTORS ───────────────────────────────────────────────────
    "servo_sg90": {
        "name": "SG90 Micro Servo",
        "category": "actuator",
        "description": "9 g micro servo, 180° rotation, 2.5 kg·cm torque, 4.8–6 V",
        "dimensions": {"w": 2.3, "h": 2.9, "d": 1.2},
        "color": "#cc4400",
        "pins": ["GND", "VCC", "PWM"]
    },
    "brushless_2204": {
        "name": "2204 Brushless Motor",
        "category": "actuator",
        "description": "2204 2300 KV brushless outrunner for 5\" quadcopters, 3–4S LiPo",
        "dimensions": {"w": 2.8, "h": 3.0, "d": 2.8},
        "color": "#cc3300",
        "pins": ["PHASE_A", "PHASE_B", "PHASE_C"]
    },
    "esc_30a": {
        "name": "30 A Brushless ESC",
        "category": "actuator",
        "description": "30 A ESC, 2–4S LiPo, BEC 5 V/3 A, SimonK/BLHeli compatible",
        "dimensions": {"w": 4.5, "h": 1.0, "d": 2.5},
        "color": "#993300",
        "pins": ["BATT_POS", "BATT_NEG", "MOTOR_A", "MOTOR_B", "MOTOR_C",
                 "SIGNAL", "BEC_5V", "BEC_GND"]
    },
    "l298n_driver": {
        "name": "L298N Motor Driver",
        "category": "actuator",
        "description": "Dual H-bridge, 2 A/channel, 5–35 V, onboard 5 V regulator",
        "dimensions": {"w": 4.3, "h": 2.7, "d": 4.3},
        "color": "#aa2200",
        "pins": ["IN1", "IN2", "IN3", "IN4", "ENA", "ENB",
                 "OUT1", "OUT2", "OUT3", "OUT4", "12V_IN", "5V_OUT", "GND"]
    },
    "relay_5v": {
        "name": "5 V Relay Module",
        "category": "actuator",
        "description": "Single-channel 5 V relay, 10 A / 250 VAC, optocoupler isolated",
        "dimensions": {"w": 3.6, "h": 1.7, "d": 2.2},
        "color": "#883300",
        "pins": ["VCC", "GND", "IN", "COM", "NO", "NC"]
    },
    "water_pump_5v": {
        "name": "Mini Water Pump 5 V",
        "category": "actuator",
        "description": "Submersible mini pump, 80–120 L/h, 5 V DC, for irrigation systems",
        "dimensions": {"w": 3.2, "h": 2.6, "d": 2.6},
        "color": "#cc5500",
        "pins": ["VCC", "GND"]
    },
    "grow_light_strip": {
        "name": "LED Grow Light Strip",
        "category": "actuator",
        "description": "Full-spectrum 12 V LED strip, 2835 SMD, 5 W/m, for plant growth",
        "dimensions": {"w": 30.0, "h": 0.3, "d": 1.0},
        "color": "#aa0066",
        "pins": ["VCC_12V", "GND"]
    },
    "dc_motor_6v": {
        "name": "DC Motor 6 V",
        "category": "actuator",
        "description": "TT gear motor, 6 V, 150 RPM, for wheeled robots and buggies",
        "dimensions": {"w": 2.8, "h": 2.8, "d": 3.5},
        "color": "#cc4400",
        "pins": ["MOTOR_POS", "MOTOR_NEG"]
    },

    # ─── POWER ────────────────────────────────────────────────────────────────
    "lipo_3s_2200": {
        "name": "3S LiPo 2200 mAh",
        "category": "power",
        "description": "11.1 V 2200 mAh 3S LiPo, 20C continuous, XT60 connector",
        "dimensions": {"w": 10.6, "h": 2.9, "d": 3.5},
        "color": "#ccaa00",
        "pins": ["XT60_POS", "XT60_NEG", "BAL_1", "BAL_2", "BAL_3", "BAL_4"]
    },
    "pdb_quadcopter": {
        "name": "Quadcopter PDB",
        "category": "power",
        "description": "Power Distribution Board, 4× ESC pads, current sensor, 5 V BEC",
        "dimensions": {"w": 5.0, "h": 0.3, "d": 5.0},
        "color": "#cc9900",
        "pins": ["BATT_POS", "BATT_NEG", "ESC1_POS", "ESC1_NEG", "ESC2_POS", "ESC2_NEG",
                 "ESC3_POS", "ESC3_NEG", "ESC4_POS", "ESC4_NEG", "5V_OUT", "GND_OUT", "CURR_OUT"]
    },
    "buck_lm2596": {
        "name": "LM2596 Buck Converter",
        "category": "power",
        "description": "Adjustable step-down DC-DC, 3–40 V in → 1.25–35 V / 3 A out",
        "dimensions": {"w": 4.5, "h": 1.4, "d": 2.1},
        "color": "#ccaa00",
        "pins": ["VIN_POS", "VIN_NEG", "VOUT_POS", "VOUT_NEG"]
    },
    "solar_panel_5v": {
        "name": "5 V Solar Panel 1 W",
        "category": "power",
        "description": "Monocrystalline 5 V / 200 mA panel, 138 × 60 mm, for IoT nodes",
        "dimensions": {"w": 13.8, "h": 0.3, "d": 6.0},
        "color": "#334455",
        "pins": ["POS", "NEG"]
    },
    "usb_powerbank": {
        "name": "USB Power Bank 10 000 mAh",
        "category": "power",
        "description": "Li-ion power bank, 5 V / 2.1 A USB-A, USB-C in, pass-through charging",
        "dimensions": {"w": 9.0, "h": 2.0, "d": 6.2},
        "color": "#ccaa00",
        "pins": ["USB_A_POS", "USB_A_NEG"]
    },

    # ─── COMMUNICATION ────────────────────────────────────────────────────────
    "hc05_bluetooth": {
        "name": "HC-05 Bluetooth",
        "category": "communication",
        "description": "Bluetooth 2.0 SPP UART module, 10 m range, AT-command configurable",
        "dimensions": {"w": 3.4, "h": 0.9, "d": 1.3},
        "color": "#7722cc",
        "pins": ["VCC", "GND", "TXD", "RXD", "STATE", "EN"]
    },
    "nrf24l01_pa": {
        "name": "nRF24L01+ PA/LNA",
        "category": "communication",
        "description": "2.4 GHz transceiver with PA+LNA, up to 1 100 m range, SPI, 2 Mbps",
        "dimensions": {"w": 4.0, "h": 0.3, "d": 1.7},
        "color": "#7722cc",
        "pins": ["GND", "VCC", "CE", "CSN", "SCK", "MOSI", "MISO", "IRQ"]
    },
    "rc_receiver_6ch": {
        "name": "6-CH RC Receiver",
        "category": "communication",
        "description": "2.4 GHz FHSS 6-channel PWM/PPM receiver with SBUS output",
        "dimensions": {"w": 3.8, "h": 1.2, "d": 2.0},
        "color": "#5511aa",
        "pins": ["CH1_AIL", "CH2_ELE", "CH3_THR", "CH4_RUD",
                 "CH5_AUX1", "CH6_AUX2", "VCC", "GND", "SBUS"]
    },
    "lora_e22": {
        "name": "E22 LoRa Module",
        "category": "communication",
        "description": "SX1262 LoRa, 433/868/915 MHz, up to 5 km, UART, -148 dBm sensitivity",
        "dimensions": {"w": 2.4, "h": 0.3, "d": 1.4},
        "color": "#7722cc",
        "pins": ["VCC", "GND", "TXD", "RXD", "M0", "M1", "AUX"]
    },

    # ─── DISPLAY ──────────────────────────────────────────────────────────────
    "oled_096": {
        "name": "0.96\" OLED 128×64",
        "category": "display",
        "description": "SSD1306 I2C OLED, 128×64 px, white/blue, 3.3–5 V, wide viewing angle",
        "dimensions": {"w": 2.7, "h": 0.2, "d": 2.7},
        "color": "#cc2288",
        "pins": ["VCC", "GND", "SCL", "SDA"]
    },
    "lcd_1602_i2c": {
        "name": "LCD 16×2 with I2C",
        "category": "display",
        "description": "16×2 character LCD with PCF8574 I2C backpack, backlit, 2.5–6 V",
        "dimensions": {"w": 8.0, "h": 1.4, "d": 3.6},
        "color": "#cc2288",
        "pins": ["VCC", "GND", "SCL", "SDA"]
    },

    # ─── PASSIVE COMPONENTS ───────────────────────────────────────────────────
    "resistor_10k": {
        "name": "Resistor 10 kΩ ¼W",
        "category": "passive",
        "description": "Carbon-film resistor, 10 kΩ, ±5 %, ¼ W through-hole",
        "dimensions": {"w": 0.6, "h": 0.3, "d": 0.2},
        "color": "#555555",
        "pins": ["A", "B"]
    },
    "capacitor_100uf": {
        "name": "Capacitor 100 µF 25 V",
        "category": "passive",
        "description": "Electrolytic decoupling cap, 100 µF 25 V, 105 °C rated",
        "dimensions": {"w": 0.8, "h": 1.5, "d": 0.8},
        "color": "#555555",
        "pins": ["POS", "NEG"]
    },
    "led_rgb": {
        "name": "RGB LED 5 mm",
        "category": "passive",
        "description": "Common-cathode 5 mm RGB LED, 20 mA/channel, 120° viewing angle",
        "dimensions": {"w": 0.5, "h": 0.9, "d": 0.5},
        "color": "#dd4488",
        "pins": ["RED", "GREEN", "BLUE", "GND"]
    },
    "buzzer_active": {
        "name": "Active Buzzer 5 V",
        "category": "passive",
        "description": "Self-oscillating piezo buzzer, 5 V, 85 dB, 2.3 kHz continuous tone",
        "dimensions": {"w": 1.2, "h": 1.0, "d": 1.2},
        "color": "#333333",
        "pins": ["POS", "NEG"]
    },
}

MOUSER_SEARCH_KEYWORDS = {
    "arduino_uno": "Arduino Uno R3 ATmega328P",
    "esp32_devkit": "ESP32-DevKitC-32E",
    "raspberry_pi_pico": "Raspberry Pi Pico RP2040",
    "flight_controller_f4": "STM32F405 flight controller",
    "raspberry_pi_4b": "Raspberry Pi 4 Model B 4GB",
    "dht22": "DHT22 AM2302 temperature humidity sensor",
    "mpu6050": "MPU-6050 6-axis gyroscope accelerometer",
    "hc_sr04": "HC-SR04 ultrasonic distance sensor",
    "bmp280": "BMP280 barometric pressure sensor",
    "soil_moisture_sensor": "capacitive soil moisture sensor",
    "pir_hcsr501": "HC-SR501 PIR motion sensor",
    "neo_6m_gps": "NEO-6M GPS module u-blox",
    "ph_sensor": "pH sensor module analog BNC",
    "water_level_sensor": "water level sensor module",
    "lm35_temp": "LM35DZ temperature sensor TO-92",
    "servo_sg90": "SG90 micro servo 9g",
    "brushless_2204": "2204 brushless motor 2300KV",
    "esc_30a": "30A brushless ESC BLHeli",
    "l298n_driver": "L298N dual H-bridge motor driver",
    "relay_5v": "5V relay module optocoupler",
    "water_pump_5v": "submersible mini water pump 5V DC",
    "grow_light_strip": "LED grow light strip full spectrum 12V",
    "dc_motor_6v": "TT gear motor 6V DC robot",
    "lipo_3s_2200": "3S LiPo battery 2200mAh 11.1V XT60",
    "pdb_quadcopter": "quadcopter power distribution board PDB",
    "buck_lm2596": "LM2596 buck converter step-down DC-DC",
    "solar_panel_5v": "5V 1W monocrystalline solar panel",
    "usb_powerbank": "USB power bank 10000mAh",
    "hc05_bluetooth": "HC-05 Bluetooth module UART",
    "nrf24l01_pa": "nRF24L01+ PA LNA 2.4GHz transceiver",
    "rc_receiver_6ch": "6 channel RC receiver 2.4GHz FHSS",
    "lora_e22": "E22 LoRa SX1262 433MHz UART module",
    "oled_096": "SSD1306 OLED 0.96 inch 128x64 I2C",
    "lcd_1602_i2c": "LCD 16x2 I2C PCF8574 backlight",
    "resistor_10k": "resistor 10k ohm 1/4W through-hole",
    "capacitor_100uf": "capacitor 100uF 25V electrolytic",
    "led_rgb": "RGB LED 5mm common cathode",
    "buzzer_active": "active buzzer 5V piezo 85dB",
}

for component_id, search_keyword in MOUSER_SEARCH_KEYWORDS.items():
    if component_id in COMPONENT_DATABASE:
        COMPONENT_DATABASE[component_id]["mouser_search"] = search_keyword

# Category metadata for frontend display
CATEGORY_META = {
    "microcontroller": {"label": "Microcontroller", "color": "#1a6bcc", "icon": "💻"},
    "sensor":          {"label": "Sensor",          "color": "#008855", "icon": "📡"},
    "actuator":        {"label": "Actuator",         "color": "#cc4400", "icon": "⚙️"},
    "power":           {"label": "Power",            "color": "#ccaa00", "icon": "⚡"},
    "communication":   {"label": "Communication",    "color": "#7722cc", "icon": "📶"},
    "display":         {"label": "Display",          "color": "#cc2288", "icon": "🖥️"},
    "passive":         {"label": "Passive",          "color": "#555555", "icon": "🔧"},
}
