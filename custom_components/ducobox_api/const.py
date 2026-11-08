"""Constants for the DucoBox integration."""

from homeassistant.const import Platform

DOMAIN = "ducobox_api"

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.FAN,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SENSOR,
]

DUCOBOX_VENTILATION_MODES = [
    "AUTO",
    "MANU",
]

DUCOBOX_NODE_TYPE_BOX = "BOX"  # Box
DUCOBOX_NODE_TYPE_BSCO2 = "BSCO2"  # CO2 sensor wired to the box PCB
DUCOBOX_NODE_TYPE_BSRH = "BSRH"  # Relative humidity sensor wired to the box PCB
DUCOBOX_NODE_TYPE_UCBAT = "UCBAT"  # Battery-powered user control
DUCOBOX_NODE_TYPE_UCCO2 = "UCCO2"  # Wall-mounted CO2 sensor
DUCOBOX_NODE_TYPE_UCRH = "UCRH"  # Wireless humidity sensor
DUCOBOX_NODE_TYPE_VLV = "VLV"  # Valve
DUCOBOX_NODE_TYPE_VLVCO2 = "VLVCO2"  # Valve with CO2 sensor
DUCOBOX_NODE_TYPE_VLVCO2RH = "VLVCO2RH"  # Valve with CO2 and relative humidity sensor
DUCOBOX_NODE_TYPE_VLVRH = "VLVRH"  # Valve with relative humidity sensor
DUCOBOX_NODE_TYPE_VLVVOC = "VLVVOC"  # Valve with VOC sensor
