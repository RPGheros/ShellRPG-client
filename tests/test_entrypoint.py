from shellrpg_client.statusline.spinner import render_spinner


def test_spinner_rotates():
    assert render_spinner(0) != render_spinner(1)
