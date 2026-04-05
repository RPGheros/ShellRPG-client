from pathlib import Path

from shellrpg_client.api_client import ApiClient
from shellrpg_client.app import (
    format_matrix_conflict_detail,
    control_write_allowed,
    format_matrix_conflict_report,
    format_matrix_health_report,
    is_character_command,
    is_control_command,
    is_game_command,
    is_matrix_command,
    is_observer_safe_game_command,
    run_shell_command,
)


def test_game_command_detection_accepts_rpg_verbs() -> None:
    assert is_game_command("city build trade hall") is True
    assert is_game_command("auto battle on balanced") is True
    assert is_game_command("merchant help") is True
    assert is_game_command("cube help") is True


def test_game_command_detection_rejects_shell_commands() -> None:
    assert is_game_command("dir") is False
    assert is_game_command("Get-ChildItem") is False


def test_character_command_detection_accepts_tree_commands() -> None:
    assert is_character_command("character list") is True
    assert is_character_command("char use 2") is True
    assert is_character_command("dir") is False


def test_control_command_detection_accepts_role_commands() -> None:
    assert is_control_command("control status") is True
    assert is_control_command("controller take") is True
    assert is_control_command("git status") is False


def test_matrix_command_detection_accepts_matrix_diagnostics() -> None:
    assert is_matrix_command("matrix health") is True
    assert is_matrix_command("matrix peers") is True
    assert is_matrix_command("control status") is False


def test_observer_safe_game_command_allows_read_only_catalog_paths() -> None:
    snapshot = {
        "status": {"control_mode": "controller-observer", "control_write_allowed": False},
        "command_details": [
            {"usage": "look", "aliases": ["look"], "observer_safe": True},
            {"usage": "walk north|south|west|east|x,y", "aliases": ["walk"], "observer_safe": False},
        ],
    }
    assert is_observer_safe_game_command(snapshot, "look") is True
    assert is_observer_safe_game_command(snapshot, "walk north") is False


def test_control_write_allowed_reads_status_flag() -> None:
    assert control_write_allowed({"status": {"control_mode": "controller-observer", "control_write_allowed": True}}) is True
    assert control_write_allowed({"status": {"control_mode": "controller-observer", "control_write_allowed": False}}) is False


def test_api_client_remembers_live_event_cursor_from_snapshot_payload() -> None:
    client = ApiClient.__new__(ApiClient)
    client.last_live_event_id = 0
    client.last_live_event_reason = ""

    client._remember_live_event({"status": {"live_event_id": 7, "live_event_reason": "control-takeover"}})

    assert client.last_live_event_id == 7
    assert client.last_live_event_reason == "control-takeover"


def test_matrix_health_report_surfaces_rollups_and_hotspots() -> None:
    report = {
        "health": {
            "status": "degraded",
            "reason": "stale-peers",
            "fresh_peer_count": 2,
            "stale_peer_count": 1,
            "last_sync_result": "up-to-date",
            "last_sync_tick": 42,
            "last_sync_source": "peer-a",
            "last_sync_ts": "2026-04-04T11:22:33Z",
            "character_conflict_count": 1,
            "field_merge_count": 2,
            "critical_character_conflict_count": 0,
            "max_conflict_severity": "medium",
            "max_conflict_tier": 2,
            "priority_severity_counts": {"medium": 2},
            "priority_reason_code_counts": {"inventory": 1, "progress_critical": 1},
        },
        "hotspots": {
            "top_characters": [{"character_name": "Mira", "max_severity": "medium"}],
            "reason_codes": [{"reason_code": "progress_critical", "count": 1}],
            "peers": [{"server_id": "peer-a", "relation": "ahead"}],
        },
    }
    rendered = format_matrix_health_report(report, include_hotspots=True)
    assert "Status: degraded" in rendered
    assert "Reason-Codes: inventory=1, progress_critical=1" in rendered
    assert "Charaktere: Mira (medium)" in rendered


def test_matrix_conflict_report_shows_ids_and_hidden_rollups() -> None:
    report = {
        "conflict_summary": {
            "character_conflict_count": 1,
            "critical_character_conflict_count": 0,
            "field_merge_count": 1,
        },
        "character_conflicts": [
            {
                "character_name": "Mira",
                "conflict_id": "cc-123",
                "max_severity": "medium",
                "max_tier": 2,
                "field_comparison_count": 1,
                "history": {"seen_count": 3, "still_open": True},
                "field_comparisons": [
                    {
                        "field": "inventory",
                        "field_conflict_id": "fc-456",
                        "max_severity": "medium",
                        "max_tier": 2,
                        "delta_summary": {
                            "priority_preview": [{"label": "potion=3", "reason_code": "inventory"}],
                            "hidden_priority_reason_code_counts": {"progress_critical": 2},
                        },
                    }
                ],
            }
        ],
    }
    rendered = format_matrix_conflict_report(report)
    assert "Mira [cc-123]" in rendered
    assert "inventory [fc-456]" in rendered
    assert "Verdeckt: progress_critical=2" in rendered


def test_matrix_conflict_report_accepts_text_filter() -> None:
    report = {
        "conflict_summary": {
            "character_conflict_count": 2,
            "critical_character_conflict_count": 1,
            "field_merge_count": 2,
        },
        "character_conflicts": [
            {
                "character_name": "Mira",
                "conflict_id": "cc-123",
                "max_severity": "critical",
                "max_tier": 4,
                "field_comparison_count": 1,
                "field_comparisons": [
                    {
                        "field": "progress_flags",
                        "field_conflict_id": "fc-111",
                        "max_severity": "critical",
                        "max_tier": 4,
                        "delta_summary": {"priority_preview": [{"label": "unlock:gate=1", "reason_code": "progress_critical"}]},
                    }
                ],
            },
            {
                "character_name": "Rook",
                "conflict_id": "cc-999",
                "max_severity": "low",
                "max_tier": 1,
                "field_comparison_count": 1,
                "field_comparisons": [
                    {
                        "field": "journal",
                        "field_conflict_id": "fc-222",
                        "max_severity": "low",
                        "max_tier": 1,
                        "delta_summary": {"priority_preview": [{"label": "Note", "reason_code": "journal"}]},
                    }
                ],
            },
        ],
    }
    rendered = format_matrix_conflict_report(report, query="critical")
    assert "Filter: critical" in rendered
    assert "Mira [cc-123]" in rendered
    assert "Rook [cc-999]" not in rendered


def test_matrix_conflict_detail_shows_preferred_fallback_and_priority_reasons() -> None:
    report = {
        "character_conflicts": [
            {
                "character_name": "Mira",
                "conflict_id": "cc-123",
                "max_severity": "high",
                "max_tier": 3,
                "history": {"seen_count": 2, "still_open": True},
                "merged_field_groups": [{"group": "inventory"}, {"group": "progress"}],
                "severity_counts": {"high": 1},
                "reason_code_counts": {"inventory": 1, "progress_critical": 1},
                "field_comparisons": [
                    {
                        "field": "inventory",
                        "field_conflict_id": "fc-456",
                        "group": "inventory",
                        "merge_mode": "winner-plus-missing",
                        "winner_side": "preferred",
                        "max_severity": "medium",
                        "max_tier": 2,
                        "severity_counts": {"medium": 1},
                        "reason_code_counts": {"inventory": 1},
                        "preferred": {"preview": ["torch=2"], "count": 1},
                        "fallback": {"preview": ["potion=3", "torch=1"], "count": 2},
                        "merged": {"preview": ["potion=3", "torch=2"], "count": 2},
                        "delta_summary": {
                            "delta_count": 2,
                            "added_count": 1,
                            "changed_count": 1,
                            "added_preview": ["potion=3"],
                            "changed_preview": ["torch:1->2"],
                            "priority_preview": [
                                {
                                    "delta_kind": "plus",
                                    "label": "potion=3",
                                    "reason_code": "inventory",
                                    "reason": "zusaetzlicher Inventargegenstand",
                                    "severity": "medium",
                                    "tier": 2,
                                    "weight": 53,
                                }
                            ],
                        },
                    }
                ],
            }
        ]
    }
    rendered = format_matrix_conflict_detail(report, "cc-123")
    assert "Mira [cc-123]" in rendered
    assert "Preferred: torch=2" in rendered
    assert "Fallback: potion=3, torch=1" in rendered
    assert "Gemerged: potion=3, torch=2" in rendered
    assert "Plus potion=3" in rendered
    assert "zusaetzlicher Inventargegenstand" in rendered


def test_matrix_conflict_detail_can_match_field_conflict_id() -> None:
    report = {
        "character_conflicts": [
            {
                "character_name": "Mira",
                "conflict_id": "cc-123",
                "field_comparisons": [
                    {
                        "field": "inventory",
                        "field_conflict_id": "fc-456",
                        "group": "inventory",
                        "merge_mode": "winner-plus-missing",
                        "winner_side": "preferred",
                        "preferred": {"preview": ["torch=2"], "count": 1},
                        "fallback": {"preview": ["potion=3", "torch=1"], "count": 2},
                        "merged": {"preview": ["potion=3", "torch=2"], "count": 2},
                        "delta_summary": {"delta_count": 1, "added_count": 1, "changed_count": 0},
                    },
                    {
                        "field": "journal",
                        "field_conflict_id": "fc-789",
                        "group": "knowledge",
                        "merge_mode": "union",
                        "winner_side": "fallback",
                        "preferred": {"preview": ["Start"], "count": 1},
                        "fallback": {"preview": ["Fallback Note"], "count": 1},
                        "merged": {"preview": ["Start", "Fallback Note"], "count": 2},
                        "delta_summary": {"delta_count": 1, "added_count": 1, "changed_count": 0},
                    },
                ],
            }
        ]
    }
    rendered = format_matrix_conflict_detail(report, "fc-456")
    assert "inventory [fc-456]" in rendered
    assert "journal [fc-789]" not in rendered


def test_run_shell_command_pwd_returns_current_directory() -> None:
    cwd = Path.cwd()
    next_cwd, output = run_shell_command("pwd", cwd)
    assert next_cwd == cwd
    assert output == str(cwd)
