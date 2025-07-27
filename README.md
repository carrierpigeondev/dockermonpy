# DockerMonPy

## Setup / Dependencies
Make sure you have a configuration file in `~/.config/dockermonpy/config.toml`

`main.py` requires either Python 3.11 or newer for use with `tomllib` (built-in) or an older Python version with `tomli` installed.

`main.py` attempts to run `lib/DockerIndicator.py` using the `python3` command. `lib/DockerIndicator.py` requires suitable PyGObject bindings, typically included in the default Python installation on your system (`python3`). If it is unavailble, you may receieve an error similar to the following:
```
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/usr/lib/python3/dist-packages/gi/__init__.py", line 40, in <module>
    from . import _gi
ImportError: cannot import name '_gi' from partially initialized module 'gi' (most likely due to a circular import) (/usr/lib/python3/dist-packages/gi/__init__.py)
```

You will also need a suitable library to display the system tray indicators for your display environment. This will differ for individual users. The code by default uses `AyatanaAppIndicator3`, however, if you need to use a different library, modify the necessary lines in `lib/DockerIndicator.py`.

```py
# Defaults
gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import AyatanaAppIndicator3 as AppIndicator3
```

## Configuration
Example `~/.config/dockermonpy/config.toml`:
```toml
[[container]]
name = "WinApps"
icon_path = "./assets/win11.png"

[[container]]
name = "Minecraft-Server"
icon_path = "./assets/mc.png"
```

Ensure the `name` is the exact name of the Docker container you are wanting to check. (i.e. the `NAMES` output from `docker ps`):
```
CONTAINER ID   IMAGE                           COMMAND                  CREATED       STATUS          PORTS                                                                                                                                   NAMES
af7f06b46279   ghcr.io/dockur/windows:latest   "/usr/bin/tini -s /r…"   6 hours ago   Up 50 minutes   0.0.0.0:3389->3389/tcp, [::]:3389->3389/tcp, 0.0.0.0:8006->8006/tcp, 0.0.0.0:3389->3389/udp, [::]:8006->8006/tcp, [::]:3389->3389/udp   WinApps
```

The `./assets` directory is a custom directory `~/.config/dockermonpy/config/assets`. The path *should* be resolved in `main.py` with Pathlib. If it fails to load the icon, try using an absolute path from inside the `config.toml`.

In this scenario, since `Minecraft-Server` is not up, the system tray icon will not appear, but `lib/DockerIndicator.DockerIndicator` checks every 5 seconds.