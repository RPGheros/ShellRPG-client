use std::process::Command;

pub fn can_play_gif() -> bool {
    which::which("cacaview").is_ok()
}

pub fn play_gif(path: &str) {
    // Best effort: show gif in terminal if available
    if which::which("cacaview").is_ok() {
        let _ = Command::new("cacaview")
            .arg(path)
            .status();
    }
}
