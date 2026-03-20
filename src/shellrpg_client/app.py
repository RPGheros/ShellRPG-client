from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from shellrpg_client.statusline.model import StatusLineState
from shellrpg_client.statusline.spinner import render_spinner

def build_demo_screen() -> str:
    state = StatusLineState(
        character_name="Ander",
        class_name="Kleriker",
        location_label="Graufurt-Osttor",
        active_action="idle",
        hp_current=41,
        hp_max=52,
        tick_value=1,
    )
    return (
        f"[{state.character_name} | {state.class_name} | {state.location_label} | "
        f"HP {state.hp_current}/{state.hp_max} | Aktion: {state.active_action} | Tick {state.tick_value}] "
        f"{render_spinner(0)}"
    )

if __name__ == "__main__":
    print(build_demo_screen())
