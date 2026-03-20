DOTS = ["●", "○", "○", "○", "○"]


def render_spinner(offset: int) -> str:
    offset = offset % 5
    states = []
    for idx in range(5):
        states.append("●" if idx <= offset else "○")
    return " ".join(states)
