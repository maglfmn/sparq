import os

import pytest

from system.i18n.translation import preload_translations


@pytest.fixture
def module_name(faker):
    return str(faker.file_name(extension=None))


@pytest.fixture
def module_path(app, module_name):
    return os.path.join(app.root_path, "modules", module_name, "lang")


def test_preload_translations__translations_exist(module_path, fs, module_name):
    fs.create_file(os.path.join(module_path, "es.json"), contents='{"Settings": "Configuración"}')
    fs.create_file(os.path.join(module_path, "fr.json"), contents='{"Settings": "Paramètres"}')
    actual_translations = preload_translations()
    assert actual_translations["es"][module_name]["Settings"] == "Configuración"
    assert actual_translations["fr"][module_name]["Settings"] == "Paramètres"


def test_preload_translations__translations_empty(module_path, fs, module_name):
    fs.create_file(os.path.join(module_path, "es.json"), contents="{}")
    actual_translations = preload_translations()
    assert actual_translations["es"][module_name] == {}


def test_preload_translations__translations_missing(module_path, fs):
    fs.create_file(os.path.join(module_path, "es.txt"))
    actual_translations = preload_translations()
    assert actual_translations == {}
