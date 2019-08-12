units = {
            'mass': {
                'mg': 0.001, 
                'kg': 1000.0, 
                'lb': 454, 
                'g': 1.0,
            },
            'volume': {
                'ml': 1.0, 
                'l': 1000.0,
                'cups': 250.0
            }
        }

base_mass = 'g'
base_volume = 'ml'

class Measurement:

    def __init__(self, s=None, value=None, unit_type='unset', density=None):
        self.value = value
        self.type = unit_type
        self.density = density

        if not s:
            return

        value_string = ""

        for i, c in enumerate(s):
            try:
                int(c)
                value_string += c
            except ValueError:
                if c == ".":
                    value_string += c
                else:
                    self.unit = s[i:]
                    break

        self.value = float(value_string)

        for unit_type_name, unit_conversions in units.items():
            if self.unit in unit_conversions:
                self.type = unit_type_name
                break
        self.value *= units[self.type][self.unit]


    def __add__(self, other):
        if self.type != other.type: 
            raise Exception("cannot add mass to volume!")
        rv = Measurement(
             value = (self.value + other.value), 
             unit_type = self.type,
             density = self.density)
        return rv





