use crossterm::terminal;
use engine_core::{events::GameEvent, GameState};
use std::time::Duration;
use tokio::{io::{AsyncReadExt}, sync::mpsc};

mod term;
mod caca;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // raw mode for “live prompt”
    terminal::enable_raw_mode()?;
    let mut ui = term::TermUi::new();

    let mut state = GameState::new("Roman");

    let (tx, mut rx) = mpsc::channel::<String>(64);

    // input task (reads bytes, builds line on Enter)
    tokio::spawn(async move {
        let mut stdin = tokio::io::stdin();
        let mut buf = [0u8; 1];
        let mut line = String::new();
        loop {
            if stdin.read_exact(&mut buf).await.is_err() {
                break;
            }
            let b = buf[0];
            match b {
                b'\r' | b'\n' => {
                    let _ = tx.send(line.clone()).await;
                    line.clear();
                }
                8 | 127 => { line.pop(); } // backspace
                _ => {
                    if b.is_ascii() {
                        line.push(b as char);
                    }
                }
            }
        }
    });

    let mut input_buf = String::new();
    let mut prompt = shell_prompt();

    // tick loop: every second redraw, every 60 seconds apply tick
    let mut elapsed = 0u64;

    loop {
        // process any entered line
        while let Ok(line) = rx.try_recv() {
            // if game awaits prompt, treat line as prompt answer
            if let Some(pid) = state.awaiting_input.clone() {
                let (events, _) = state.answer_prompt(&pid, &line);
                for e in events {
                    show_event(&mut ui, &e, true);
                }
            } else {
                // free command mode
                let events = state.handle_command(&line);
                for e in events {
                    show_event(&mut ui, &e, true);
                }
            }
            input_buf.clear();
        }

        // tick every 60 seconds
        if elapsed % state.tick_seconds == 0 {
            let events = state.tick();
            for e in events {
                show_event(&mut ui, &e, false);
            }
        }

        // update prompt based on whether input is needed
        prompt = if state.awaiting_input.is_some() {
            // during prompts we “swap out the shell prompt”:
            "".to_string()
        } else {
            shell_prompt()
        };

        // action line + spinner/progress
        let spin = ui.tick_spinner();
        let action = if state.awaiting_input.is_some() {
            // show that we are waiting
            "Input required…".to_string()
        } else {
            // show status like your sample
            let p = active_progress_percent(&state);
            format!("{} {} {:>3}%", state.knight.current_action_de, spin, p)
        };

        // render
        ui.render(&action, &prompt, &input_buf)?;

        tokio::time::sleep(Duration::from_secs(1)).await;
        elapsed += 1;
    }
}

fn active_progress_percent(state: &GameState) -> i32 {
    state.knight.tasks.iter().find(|t| t.active).map(|t| t.progress as i32).unwrap_or(0)
}

fn show_event(ui: &mut term::TermUi, e: &GameEvent, german: bool) {
    match e {
        GameEvent::Log { en, de } => ui.push_line(if german { de } else { en }),
        GameEvent::GifScene { gif_path, en, de } => {
            // show gif if possible
            if crate::caca::can_play_gif() {
                crate::caca::play_gif(gif_path);
            }
            ui.push_line(if german { de } else { en });
        }
        GameEvent::Prompt(p) => {
            // dump prompt into rolling log lines; prompt itself is drawn by “prompt swap”
            ui.push_line(if german { p.text_de.clone() } else { p.text_en.clone() });
        }
        GameEvent::CombatEncounter { enemy_id } => {
            ui.push_line(format!("Encounter: {}", enemy_id));
        }
    }
}

fn shell_prompt() -> String {
    // keep it simple; can be customized by OS.
    "[user@host /directory]: ".to_string()
}
