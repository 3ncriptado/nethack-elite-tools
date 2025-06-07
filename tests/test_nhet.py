import sys
import types
import os
from unittest.mock import patch

# Provide dummy modules for dependencies not installed in the testing environment
customtkinter = types.ModuleType("customtkinter")
customtkinter.CTk = type("CTk", (), {})
customtkinter.CTkEntry = object
customtkinter.CTkFrame = object
customtkinter.CTkButton = object
customtkinter.CTkTextbox = object
customtkinter.set_appearance_mode = lambda *a, **k: None
customtkinter.set_default_color_theme = lambda *a, **k: None

matplotlib = types.ModuleType("matplotlib")
matplotlib.use = lambda *a, **k: None
matplotlib_pyplot = types.ModuleType("pyplot")
matplotlib_backends = types.ModuleType("matplotlib.backends.backend_tkagg")
matplotlib_backends.FigureCanvasTkAgg = object

sys.modules.setdefault("customtkinter", customtkinter)
sys.modules.setdefault("matplotlib", matplotlib)
sys.modules.setdefault("matplotlib.pyplot", matplotlib_pyplot)
sys.modules.setdefault("matplotlib.backends.backend_tkagg", matplotlib_backends)
sys.modules.setdefault("requests", types.SimpleNamespace())

# Ensure project root is on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import NHET


class DummyEntry:
    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value


class DummyOutput:
    def __init__(self):
        self.text = ""

    def delete(self, start, end):
        self.text = ""

    def insert(self, index, text):
        self.text += text


def test_resolve_domain_sets_ip():
    app = NHET.NetworkToolsApp.__new__(NHET.NetworkToolsApp)
    app.domain_entry = DummyEntry("example.com")
    app.resolver_result = DummyOutput()

    with patch("socket.gethostbyname", return_value="1.2.3.4"):
        app.resolve_domain()

    assert app.resolver_result.text == "IP: 1.2.3.4"
