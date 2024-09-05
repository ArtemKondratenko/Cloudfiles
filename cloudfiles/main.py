import threading
from pathlib import Path
import os
import click
import subprocess
from monitoringparser.monitoring_list_parser import load, dump
from filesystemwatcher.main import run
from filesystemwatcher.daemon_control import stop



MONITORING_LIST: Path = Path.home() / ".local" / "share" / "cloudfiles" / "monitoring_list"


@click.command("add")
@click.argument("paths", nargs=-1, type=click.Path(exists=False, file_okay=False, dir_okay=False))
def add(paths):
    os.makedirs(MONITORING_LIST.parent, exist_ok=True)

    with open(MONITORING_LIST, 'a+') as file:
        file.seek(0)
        existing_paths = load(file)
        absolute_paths = {Path(path).absolute() for path in paths}
        if any(path not in existing_paths for path in absolute_paths):
            new_paths = absolute_paths - existing_paths
            dump(new_paths, file)
            print(f"Add path: {new_paths}")
        else:
            print(f"The path:{absolute_paths} already exists!")



@click.command("remove")
@click.argument("paths", nargs=-1, type=click.Path(exists=False, file_okay=False, dir_okay=False))
def remove(paths):
    with open(MONITORING_LIST, 'r') as file:
        existing_paths = load(file)

    paths_to_remove = {Path(path).absolute() for path in paths}
    updated_paths = existing_paths - paths_to_remove

    with open(MONITORING_LIST, 'w') as file:
        for path in updated_paths:
            file.write(str(path) + "\n")




@click.group()
def cli():
    pass

# def run_other_project():
#     env = os.environ.copy()
#     env["PYTHONPATH"] = "/home/tema/PycharmProjects/Cloudfiles"
#     subprocess.Popen(["python", "/home/tema/PycharmProjects/FileSystemWatcher/FileSystemWatcher/main.py"], env=env)


cli.add_command(add)
cli.add_command(remove)

if __name__ == "__main__":
    # Создание директории и файла, если они не существуют
    os.makedirs(MONITORING_LIST.parent, exist_ok=True)
    if not MONITORING_LIST.exists():
        with open(MONITORING_LIST, 'w') as f:
            pass  # Создание пустого файла

    daemon_thread = threading.Thread(target=run, args=(MONITORING_LIST,))
    daemon_thread.start()

    try:
        cli()  # Запуск командной строки
    finally:
        stop()  # Остановка демона при завершении
        daemon_thread.join()  # Ждем завершения потока демона
