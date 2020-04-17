import os
from conans import ConanFile, CMake, tools

class LinuxdeployBundleQtTestConan(ConanFile):
    settings = {"os": ["Linux"], "arch": None}
    def build(self):
        pass

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("linuxdeploy --help", run_environment=True)
            self.run("linuxdeploy --list-plugins", run_environment=True)
