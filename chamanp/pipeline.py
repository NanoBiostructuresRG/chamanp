# SPDX-License-Identifier: LGPL-3.0-or-later
"""Public execution doorway for CHAMANP."""

from chamanp.config import ChamanpConfig
from chamanp.result import ChamanpResult


def validate_config(config: ChamanpConfig | None = None) -> ChamanpConfig:
    """Validate a CHAMANP runtime configuration object."""
    active_config = ChamanpConfig() if config is None else config
    return _validate_config_impl(active_config)


def run(config: ChamanpConfig | None = None) -> ChamanpResult:
    """Validate and execute CHAMANP, writing configured artifacts to disk."""
    active_config = validate_config(config)
    pipeline = _pipeline_cls()(config=active_config)
    return pipeline.run()


def _validate_config_impl(config):
    from chamanp._core.preflight import validate_config as _validate_config

    return _validate_config(config)


def _pipeline_cls():
    from chamanp._core.base_pipeline import Pipeline

    return Pipeline


__all__ = ["validate_config", "run"]
