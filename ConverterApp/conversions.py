# conversions.py

TEMPERATURE_UNITS = [
    "Celsius",
    "Fahrenheit",
    "Kelvin"
]

CONVERSION_FACTORS = {
    "Length": {
        "Millimeter": 0.001,
        "Centimeter": 0.01,
        "Meter": 1,
        "Kilometer": 1000,
        "Inch": 0.0254,
        "Foot": 0.3048,
        "Yard": 0.9144,
        "Mile": 1609.344
    },

    "Weight": {
        "Milligram": 0.001,
        "Gram": 1,
        "Kilogram": 1000,
        "Ounce": 28.349523125,
        "Pound": 453.59237,
        "Ton": 1_000_000
    },

    "Volume": {
        "Milliliter": 0.001,
        "Liter": 1,
        "Cup": 0.236588,
        "Pint": 0.473176,
        "Quart": 0.946353,
        "Gallon": 3.78541
    },

    "Time": {
        "Millisecond": 0.001,
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800
    },

    "Area": {
        "Square Millimeter": 0.000001,
        "Square Centimeter": 0.0001,
        "Square Meter": 1,
        "Square Kilometer": 1_000_000,
        "Square Foot": 0.09290304,
        "Square Yard": 0.83612736,
        "Acre": 4046.8564224,
        "Hectare": 10000
    },

    "Speed": {
        "Meters/Second": 1,
        "Kilometers/Hour": 0.277777778,
        "Miles/Hour": 0.44704,
        "Knot": 0.514444
    },

    # Supports both decimal and binary storage units
    "Data Storage": {
        "Byte": 1,

        "Kilobyte (KB)": 1000,
        "Megabyte (MB)": 1000 ** 2,
        "Gigabyte (GB)": 1000 ** 3,
        "Terabyte (TB)": 1000 ** 4,

        "Kibibyte (KiB)": 1024,
        "Mebibyte (MiB)": 1024 ** 2,
        "Gibibyte (GiB)": 1024 ** 3,
        "Tebibyte (TiB)": 1024 ** 4,
    }
}


UNITS = {
    "Temperature": TEMPERATURE_UNITS
}

for category, units in CONVERSION_FACTORS.items():
    UNITS[category] = list(units.keys())


UNIT_TO_CATEGORY = {
    unit: category
    for category, units in UNITS.items()
    for unit in units
}


CATEGORY_ICONS = {
    "Temperature": "🌡",
    "Length": "📏",
    "Weight": "⚖",
    "Volume": "🧪",
    "Time": "⏱",
    "Area": "▢",
    "Speed": "🚗",
    "Data Storage": "💾"
}


def convert_temperature(value, from_unit, to_unit):
    """
    Convert between temperature units.
    """

    # Convert to Celsius first
    if from_unit == "Celsius":
        celsius = value

    elif from_unit == "Fahrenheit":
        celsius = (value - 32) * 5 / 9

    elif from_unit == "Kelvin":
        celsius = value - 273.15

    else:
        raise ValueError(
            f"Unsupported temperature unit: {from_unit}"
        )

    # Convert from Celsius to target
    if to_unit == "Celsius":
        return celsius

    elif to_unit == "Fahrenheit":
        return celsius * 9 / 5 + 32

    elif to_unit == "Kelvin":
        return celsius + 273.15

    raise ValueError(
        f"Unsupported temperature unit: {to_unit}"
    )


def convert_value(value, from_unit, to_unit):
    """
    Convert between compatible units.
    """

    category = UNIT_TO_CATEGORY[from_unit]

    if category == "Temperature":
        return convert_temperature(
            value,
            from_unit,
            to_unit
        )

    factors = CONVERSION_FACTORS[category]

    base_value = value * factors[from_unit]

    return base_value / factors[to_unit]