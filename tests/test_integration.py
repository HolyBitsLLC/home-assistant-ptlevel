"""Tests for PTLevel Home Assistant integration."""

import json
import pytest
from pathlib import Path

COMPONENT_DIR = Path(__file__).parent.parent / "custom_components" / "ptlevel"


def test_manifest_valid():
    """Verify manifest.json is valid JSON and has required fields."""
    manifest = json.loads((COMPONENT_DIR / "manifest.json").read_text())
    assert manifest["domain"] == "ptlevel"
    assert "name" in manifest
    assert manifest.get("iot_class") == "cloud_polling"
    assert manifest.get("config_flow") is True


def test_strings_valid():
    """Verify strings.json is valid JSON."""
    strings = json.loads((COMPONENT_DIR / "strings.json").read_text())
    assert "config" in strings


def test_translations_valid():
    """Verify translations/en.json is valid JSON."""
    translations = json.loads(
        (COMPONENT_DIR / "translations" / "en.json").read_text()
    )
    assert "config" in translations


def test_constants():
    """Verify const.py has required constants."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "const", COMPONENT_DIR / "const.py"
    )
    const = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(const)
    assert const.DOMAIN == "ptlevel"
    assert const.CONF_USERNAME == "username"
    assert const.CONF_PASSWORD == "password"


def test_services_yaml_exists():
    """Verify services.yaml exists (even if mostly commented)."""
    assert (COMPONENT_DIR / "services.yaml").exists()
