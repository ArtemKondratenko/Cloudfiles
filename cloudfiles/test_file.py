from cloudfiles.main import add, remove, MONITORING_LIST
from monitoringparser.monitoring_list_parser import load
from pathlib import Path
from click.testing import CliRunner


def test_add():
    runner = CliRunner()

    runner.invoke(add, ["mkdir1"])
    with open(MONITORING_LIST, 'r') as file:
        assert load(file) == {Path("mkdir1").absolute()}

    runner.invoke(add, ["mkdir1", "mkdir2"])
    with open(MONITORING_LIST, 'r') as file:
        assert  load(file) == {Path("mkdir1").absolute(), Path("mkdir2").absolute()}

    runner.invoke(add, [])
    with open(MONITORING_LIST, 'r') as file:
        assert load(file) == {Path("mkdir1").absolute(), Path("mkdir2").absolute()}

    result = runner.invoke(add, ["mkdir4"])
    assert result.exit_code == 0

def test_remove():
    runner = CliRunner()

    runner.invoke(remove, ["mkdir1"])
    with open(MONITORING_LIST, 'r') as file:
        assert load(file) == {Path("mkdir2").absolute(), Path("mkdir4").absolute()}

    runner.invoke(remove, ["mkdir4"])
    with open(MONITORING_LIST, 'r') as file:
        assert load(file) == {Path("mkdir2").absolute()}

    runner.invoke(remove, ["mkdir2"])
    with open(MONITORING_LIST, 'r') as file:
        assert load(file) == set()