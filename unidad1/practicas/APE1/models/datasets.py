"""Static data for the atmospheric-rainfall model (APE1).

Holds the temperature-factor table, the model coefficients and the hourly
observations defined in the practice guide.
"""

# Temperature factor (Tf) by temperature in Celsius, as given by the guide.
tabla_tf = {
    10: 1.00,
    12: 0.90,
    14: 0.80,
    16: 0.70,
    18: 0.60,
    20: 0.50,
    22: 0.40,
    24: 0.30,
    26: 0.20,
    28: 0.10,
}

# Coefficients of the atmospheric index I = aH + bN + cTf.
# Original model from the guide.
COEFICIENTES_ORIGINAL = {"H": 0.50, "N": 0.30, "Tf": 0.20}

# Adjusted model: randomly chosen coefficients that still add up to 1.0.
COEFICIENTES_AJUSTADO = {"H": 0.40, "N": 0.35, "Tf": 0.25}

# Hourly observations: (hora, humedad %, nubosidad %, temperatura °C).
DATOS_HORARIOS = [
    ("06:00", 65, 40, 14),
    ("08:00", 70, 50, 16),
    ("10:00", 68, 45, 18),
    ("12:00", 60, 30, 22),
    ("14:00", 75, 70, 20),
    ("16:00", 85, 85, 18),
    ("18:00", 92, 95, 16),
    ("20:00", 88, 90, 17),
    ("22:00", 80, 75, 15),
]

# Rain rules as (upper bound, state); the last rule has an open upper bound.
REGLAS_LLUVIA = [
    (0.40, "Sin lluvia"),
    (0.60, "Baja posibilidad"),
    (0.75, "Lluvia probable"),
    (None, "Lluvia"),
]
