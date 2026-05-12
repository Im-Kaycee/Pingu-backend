import platform
import subprocess
import shutil
import os

def get_system_info() -> dict:
    info = {}

    # Distro info
    try:
        with open("/etc/os-release") as f:
            for line in f:
                k, _, v = line.partition("=")
                info[k.strip()] = v.strip().strip('"')
    except FileNotFoundError:
        pass

    info["os_name"] = info.get("NAME", "Linux")
    info["os_version"] = info.get("VERSION_ID", "unknown")
    info["os_codename"] = info.get("VERSION_CODENAME", "unknown")
    info["architecture"] = platform.machine()
    info["kernel"] = platform.release()
    info["is_wsl"] = "microsoft" in platform.release().lower()
    info["shell"] = os.environ.get("SHELL", "/bin/bash")
    info["home"] = os.environ.get("HOME", "")
    info["user"] = os.environ.get("USER", "")
    info["package_manager"] = _detect_package_manager()
    info["has_sudo"] = shutil.which("sudo") is not None
    info["has_snap"] = shutil.which("snap") is not None
    info["has_flatpak"] = shutil.which("flatpak") is not None
    info["has_docker"] = shutil.which("docker") is not None
    info["has_git"] = shutil.which("git") is not None
    info["has_python3"] = shutil.which("python3") is not None
    info["has_node"] = shutil.which("node") is not None
    info["has_ollama"] = shutil.which("ollama") is not None

    return info

def _detect_package_manager() -> str:
    for pm in ["apt", "dnf", "pacman", "zypper"]:
        if shutil.which(pm):
            return pm
    return "unknown"
