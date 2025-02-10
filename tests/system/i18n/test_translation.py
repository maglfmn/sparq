import os

import pytest

from system.i18n.translation import preload_translations


@pytest.fixture
def core_path(app):
    return os.path.join(app.root_path, "modules", "core", "lang")


def test_preload_translations__translations_exist(core_path, fs):
    fs.create_file(os.path.join(core_path, "es.json"), contents='{"Settings": "Configuración"}')
    fs.create_file(os.path.join(core_path, "fr.json"), contents='{"Settings": "Paramètres"}')
    actual_translations = preload_translations()
    assert actual_translations["es"]["core"]["Settings"] == "Configuración"
    assert actual_translations["fr"]["core"]["Settings"] == "Paramètres"


def test_preload_translations__translations_empty(core_path, fs):
    fs.create_file(os.path.join(core_path, "es.json"), contents="{}")
    actual_translations = preload_translations()
    assert actual_translations["es"]["core"] == {}


def test_preload_translations__translations_missing(core_path, fs):
    fs.create_file(os.path.join(core_path, "es.txt"))
    actual_translations = preload_translations()
    assert actual_translations == {}
