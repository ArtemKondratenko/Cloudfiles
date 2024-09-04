from pathlib import Path
import signal
import os
import click

from monitoringparser.monitoring_list_parser import load, dump



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


cli.add_command(add)
cli.add_command(remove)

if __name__ == "__main__":
    cli()
