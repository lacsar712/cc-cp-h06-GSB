"""判定回归：甲探合格、乙探超温，写入库字段不得再被粉饰。"""

import importlib.util

from rules import judge_temp
from worker import finish


class FakeConn:
    def __init__(self):
        self.queries = []
        self.committed = False

    def execute(self, sql, params=None):
        self.queries.append((sql, params))

    def commit(self):
        self.committed = True


def test_judge_pass_probe_a():
    verdict, reason = judge_temp(4.2)
    assert verdict == "合格"
    assert "未超过 8℃" in reason


def test_judge_overtemp_probe_b():
    verdict, reason = judge_temp(12.5)
    assert verdict == "超温"
    assert "超过 8℃" in reason


def test_finish_persists_pass_verdict_unpolished():
    conn = FakeConn()
    finish(conn, 1, 4.2)
    _, params = conn.queries[-1]
    assert params[0] == "合格"
    assert "未超过 8℃" in params[1]
    assert conn.committed


def test_finish_keeps_overtemp_verdict():
    conn = FakeConn()
    finish(conn, 2, 12.5)
    _, params = conn.queries[-1]
    assert params[0] == "超温"
    assert "超过 8℃" in params[1]


def test_no_polish_modules_remain():
    assert importlib.util.find_spec("pass_polish") is None
    assert importlib.util.find_spec("h06_extra_trap") is None
