import sys
import docker

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("GLib", "2.0")
from gi.repository import Gtk, GLib

gi.require_version("AyatanaAppIndicator3", "0.1")
from gi.repository import AyatanaAppIndicator3 as AppIndicator3

import setuplogger

client = docker.from_env()

def build_simple_menu():
    menu = Gtk.Menu()
    quit_item = Gtk.MenuItem(label="Quit DockerMonPy Instance")
    quit_item.connect("activate", Gtk.main_quit)
    menu.append(quit_item)
    menu.show_all()
    return menu

class DockerIndicator:
    def __init__(self, name, icon_path):
        logger = setuplogger.make_logger()
        logger.info(f"Creating DockerIndicator for {name}")

        try:
            self.name = name
            self.icon_path = icon_path

            logger.info("Creating indicator...")
            self.indicator = AppIndicator3.Indicator.new(
                "dockerindicator",
                "",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_icon_full(self.icon_path, self.name)
            self.indicator.set_menu(build_simple_menu())
            self.indicator.set_title(f"DockerMonPy - {self.name} Status")

            logger.info("Creating GLib updater...")
            GLib.timeout_add_seconds(5, self.update_status)

            logger.info("Should be set up!")

            Gtk.main()

        except Exception as e:
            logger.fatal(e)

    def update_status(self):
        if self.check():
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        else:
            self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
        return True

    def check(self):
        try:
            container = client.containers.get(self.name)
            return container.status == "running"
        
        except docker.errors.NotFound:
            return False

if __name__ == "__main__":
    name = sys.argv[1]
    icon_path = sys.argv[2]
    DockerIndicator(name, icon_path)