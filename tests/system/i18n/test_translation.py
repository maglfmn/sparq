import json
import os

import pytest
from flask import g

from system.i18n.translation import preload_translations
from system.i18n.translation import translate


@pytest.fixture
def module_name(faker):
    return str(faker.file_name(extension=""))


@pytest.fixture
def module_path(app, module_name):
    g.current_module = {"name": module_name}
    return os.path.join(app.root_path, "modules", module_name, "lang")


@pytest.fixture
def core_module_path(app):
    module_name = "core"
    g.current_module = {"name": module_name}
    return os.path.join(app.root_path, "modules", module_name, "lang")


def test_preload_translations__translations_exist(module_path, mock_fs, module_name):
    mock_fs.create_file(
        os.path.join(module_path, "es.json"),
        contents='{"Settings": "Configuración"}',
    )
    mock_fs.create_file(
        os.path.join(module_path, "fr.json"),
        contents='{"Settings": "Paramètres"}',
    )
    actual_translations = preload_translations()
    assert actual_translations["es"][module_name]["Settings"] == "Configuración"
    assert actual_translations["fr"][module_name]["Settings"] == "Paramètres"


def test_preload_translations__translations_empty(module_path, mock_fs, module_name):
    mock_fs.create_file(os.path.join(module_path, "es.json"), contents="{}")
    actual_translations = preload_translations()
    assert actual_translations["es"][module_name] == {}


def test_preload_translations__translations_missing(module_path, fs):
    fs.create_file(os.path.join(module_path, "es.txt"))
    actual_translations = preload_translations()
    assert actual_translations == {}


@pytest.mark.parametrize(
    "language,translated_value",
    [
        ("es", "Configuración"),
        ("en", "SettingsValue"),
    ],
)
def test_translate__translation_exists(mock_fs, language, module_path, translated_value):
    """Translation will take from the current module."""
    g.lang = language
    mock_fs.create_file(
        os.path.join(module_path, f"{language}.json"),
        contents=json.dumps({"SettingsKey": translated_value}),
    )
    preload_translations()
    assert translate("SettingsKey") == translated_value


@pytest.mark.parametrize(
    "language,translated_value",
    [
        ("es", "Configuración"),
        ("en", "SettingsValue"),
    ],
)
def test_translate__translation_from_core(mock_fs, language, core_module_path, translated_value):
    """Translation will take from the `core` module."""
    g.lang = language
    mock_fs.create_file(
        os.path.join(core_module_path, f"{language}.json"),
        contents=json.dumps({"SettingsKey": translated_value}),
    )
    preload_translations()
    assert translate("SettingsKey") == translated_value


@pytest.mark.parametrize("language", ["es", "en"])
def test_translate__translation_not_exists(language, module_path):
    """Translation will return the original text."""
    g.lang = language
    preload_translations()
    assert translate("SettingsKey") == "SettingsKey"
