DOTS = ["●", "●", "●", "○", "○"]

def render_spinner(offset: int) -> str:
    offset = offset % len(DOTS)
    rotated = DOTS[offset:] + DOTS[:offset]
    return " ".join(rotated)
