"""max_in_progress must be re-read every gateway tick (not frozen at boot)."""
from unittest import mock

from gateway import kanban_watchers_dispatcher as kwd


def test_tick_uses_live_max_in_progress():
    settings = kwd._DispatcherSettings(interval=60, max_spawn=None, max_in_progress=None, failure_limit=2,
                                       stale_timeout_seconds=14400, reconcile_orphans=True,
                                       default_assignee=None, max_in_progress_per_profile=None)
    d = kwd._KanbanDispatcher(mock.Mock(), settings)
    kbd = mock.Mock()
    kbd.configured_max_in_progress.return_value = 2
    kbd.resolve_max_in_progress.side_effect = lambda v: v
    kbc = mock.Mock()
    with mock.patch.object(kwd, "_kbd", return_value=kbd), mock.patch.object(kwd, "_kbc", return_value=kbc), \
         mock.patch.object(d, "board_db_fingerprint", return_value=None):
        d.tick_once_for_board("default")
    assert kbd.dispatch_once.call_args.kwargs["max_in_progress"] == 2
