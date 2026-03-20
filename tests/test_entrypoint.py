from shellrpg_client.statusline.spinner import render_spinner


def test_spinner_progresses():
    assert render_spinner(0) != render_spinner(3)
