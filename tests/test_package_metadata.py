from __future__ import annotations

import pyz1


def test_package_exports_version() -> None:
    assert pyz1.__version__ == "0.1.0"
