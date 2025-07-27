import subprocess
import pathlib
import os

try:
    import tomllib
except ImportError:
    import tomli as tomllib

CONFIG_PATH = pathlib.Path.home() / ".config" / "dockermonpy"
CONFIG_FILE = CONFIG_PATH / "config.toml"

import lib.setuplogger

def main():
    logger = lib.setuplogger.make_logger()

    logger.info("Started DockerMonPy")

    logger.info("Reading file...")
    with open(CONFIG_FILE, "rb") as f:
        config = tomllib.load(f)

    logger.info("Adding container entries...")
    for container in config["container"]:
        logger.info(f"Current entry: {container['name']}")

        icon_path = pathlib.Path(container["icon_path"])
        if not icon_path.is_absolute():
            icon_path = (CONFIG_PATH / icon_path).resolve()
        logger.info(f"Said entry's icon path is at {icon_path}")

        logger.info("Starting entry...")
        cwd = pathlib.Path(__file__).parent.resolve()
        subprocess.Popen([
            "python3",
            "lib/DockerIndicator.py",
            container["name"],
            str(icon_path)
        ], cwd=cwd)

if __name__ == "__main__":
    main()