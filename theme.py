BG = "#f2f5fb"
CARD = "#ffffff"
PRIMARY = "#3b6ef6"
PRIMARY_D = "#2b57cc"
TEXT = "#1f2937"
MUTED = "#7a8699"
ERROR = "#e03131"
OK = "#1f9d55"

def fmt(x):
    if abs(x) < 1e-12: x = 0.0
    if abs(x - round(x)) < 1e-9: return str(int(round(x)))
    return f"{x:.6f}".rstrip("0").rstrip(".")