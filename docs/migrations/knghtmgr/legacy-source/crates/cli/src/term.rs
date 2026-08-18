use crossterm::{
    cursor,
    style::{Color, Print, ResetColor, SetForegroundColor},
    terminal::{self, Clear, ClearType},
    ExecutableCommand,
};
use std::io::{stdout, Write};

pub struct TermUi {
    // last 3 lines of output
    lines: [String; 3],
    spinner_idx: usize,
    spinner: [char; 3],
}

impl TermUi {
    pub fn new() -> Self {
        Self {
            lines: ["".into(), "".into(), "".into()],
            spinner_idx: 0,
            spinner: ['.', '.', '.'],
        }
    }

    pub fn push_line(&mut self, s: impl Into<String>) {
        self.lines[0] = self.lines[1].clone();
        self.lines[1] = self.lines[2].clone();
        self.lines[2] = s.into();
    }

    pub fn tick_spinner(&mut self) -> String {
        // rotate: [.  ], [.. ], [...], [.. ], ...
        let frames = ["[.   ]", "[..  ]", "[... ]", "[..  ]"];
        self.spinner_idx = (self.spinner_idx + 1) % frames.len();
        frames[self.spinner_idx].to_string()
    }

    pub fn render(&mut self, action_line: &str, prompt: &str, input: &str) -> crossterm::Result<()> {
        let mut out = stdout();
        let (cols, rows) = terminal::size()?;

        // We draw at bottom: 4 lines: 3 output lines + prompt line
        // Place cursor at rows-4 (0-index vs 1-index handled by crossterm)
        let base_row = rows.saturating_sub(4);

        out.execute(cursor::MoveTo(0, base_row))?;
        out.execute(Clear(ClearType::FromCursorDown))?;

        // action line (status) as first of the 3 “output” lines
        // color it lightly
        out.execute(SetForegroundColor(Color::Cyan))?;
        out.execute(Print(trim_to_width(action_line, cols)))?;
        out.execute(ResetColor)?;
        out.execute(Print("\n"))?;

        // next two lines are rolling log
        for i in 1..3 {
            out.execute(Print(trim_to_width(&self.lines[i], cols)))?;
            out.execute(Print("\n"))?;
        }

        // prompt + input
        out.execute(SetForegroundColor(Color::Green))?;
        out.execute(Print(prompt))?;
        out.execute(ResetColor)?;
        out.execute(Print(input))?;

        out.flush()?;
        Ok(())
    }
}

fn trim_to_width(s: &str, cols: u16) -> String {
    let max = cols as usize;
    if s.len() <= max { return s.to_string(); }
    let mut t = s[..max.saturating_sub(1)].to_string();
    t.push('…');
    t
}
