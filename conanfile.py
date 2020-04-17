from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration
import os
import shutil

class LinuxdeployBundleQtConan(ConanFile):
    name = "linuxdeploy-bundle-qt"
    version = "continuous"
    settings = {"os": ["Linux"], "arch": None}

    def build(self):
        if (self.settings.arch == "x86" or self.settings.arch == "x86_64"):
            if self.settings.arch == "x86":
                linuxdeploy_arch = "i686"
            else:
                linuxdeploy_arch = self.settings.arch

            self._download_appimage(linuxdeploy_arch)
        else:
            raise ConanInvalidConfiguration("Unsupported arch: %s" % self.settings.arch)

    def _download_appimage(self, arch):
        tools.download("https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-%s.AppImage"
                        % (arch), "appimagetool.AppImage")
        self.run("chmod +x appimagetool.AppImage", run_environment=True)
        os.makedirs("appimagetool", exist_ok=True) 
        shutil.move("appimagetool.AppImage", "appimagetool/appimagetool.AppImage")
        self.run("cd appimagetool && ./appimagetool.AppImage --appimage-extract", run_environment=True)

        
        tools.download("https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-%s.AppImage"
                        % (arch), "linuxdeploy.AppImage")
        self.run("chmod +x linuxdeploy.AppImage", run_environment=True)
        os.makedirs("linuxdeploy", exist_ok=True) 
        shutil.move("linuxdeploy.AppImage", "linuxdeploy/linuxdeploy.AppImage")
        self.run("cd linuxdeploy && ./linuxdeploy.AppImage --appimage-extract", run_environment=True)

        tools.download("https://github.com/linuxdeploy/linuxdeploy-plugin-qt/releases/download/continuous/linuxdeploy-plugin-qt-%s.AppImage"
                        % (arch), "linuxdeploy-plugin-qt.AppImage")
        self.run("chmod +x linuxdeploy-plugin-qt.AppImage", run_environment=True)
        os.makedirs("linuxdeploy-plugin-qt", exist_ok=True) 
        shutil.move("linuxdeploy-plugin-qt.AppImage", "linuxdeploy-plugin-qt/linuxdeploy-plugin-qt.AppImage")
        self.run("cd linuxdeploy-plugin-qt && ./linuxdeploy-plugin-qt.AppImage --appimage-extract", run_environment=True)
        

    def package(self):
        self.copy("*", dst="bin", src="appimagetool/squashfs-root/usr/bin")
        self.copy("*", dst="lib", src="appimagetool/squashfs-root/usr/lib", symlinks=True)
        self.copy("*", dst="share", src="appimagetool/squashfs-root/usr/share", symlinks=True)

        self.copy("*", dst="bin", src="linuxdeploy/squashfs-root/usr/bin")
        self.copy("*", dst="lib", src="linuxdeploy/squashfs-root/usr/lib", symlinks=True)
        self.copy("*", dst="share", src="linuxdeploy/squashfs-root/usr/share", symlinks=True)

        self.copy("*", dst="bin", src="linuxdeploy-plugin-qt/squashfs-root/usr/bin")
        self.copy("*", dst="lib", src="linuxdeploy-plugin-qt/squashfs-root/usr/lib", symlinks=True)
        self.copy("*", dst="share", src="linuxdeploy-plugin-qt/squashfs-root/usr/share", symlinks=True)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "usr", "bin"))
        self.env_info.LD_LIBRARY_PATH.append(os.path.join(self.package_folder, "usr", "lib"))