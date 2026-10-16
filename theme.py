BG = "#121212"
CARD = "#1E1E1E"
PRIMARY = "#FF6B00"
TEXT = "#FFFFFF"
MUTED = "#AAAAAA"
ERROR = "#FF3333"
OK = "#00CC66"

def fmt(x):
    if abs(x) < 1e-12: x = 0.0
    if abs(x - round(x)) < 1e-9: return str(int(round(x)))
    return f"{x:.6f}".rstrip("0").rstrip(".")