# SPDX-License-Identifier: LGPL-3.0-or-later
"""Public execution doorway for CHAMANP."""

from chamanp.config import ChamanpConfig
from chamanp.result import ChamanpResult


def validate_config(config: ChamanpConfig | None = None) -> ChamanpConfig:
    """Validate a CHAMANP runtime configuration object.

    Checks that required file paths exist, that collection settings are
    well-formed, and that fingerprint parameters are valid integers.
    ``COLLECTION_LOGIC`` and ``COLLECTION_TAG`` values are normalized
    in-place (stripped and upper-cased where applicable) before the
    validated configuration is returned.

    Parameters
    ----------
    config : ChamanpConfig, optional
        Configuration to validate. When ``None``, a default
        ``ChamanpConfig`` is constructed and validated.

    Returns
    -------
    ChamanpConfig
        The validated configuration object, with ``COLLECTION_LOGIC`` and
        ``COLLECTION_TAG`` normalized.

    Raises
    ------
    chamanp._core.preflight.ConfigurationError
        If one or more validation checks fail. The error message lists all
        failing checks.

    Examples
    --------
    Validate a configuration before running the pipeline:

    >>> from chamanp import ChamanpConfig, validate_config
    >>> config = ChamanpConfig(
    ...     DATABASE_PATH="data/coconut.csv",
    ...     COLLECTION_TAXONOMY_PATH="data/taxonomy.json",
    ...     TARGET_COLLECTIONS=["PubChem NPs"],
    ...     COLLECTION_TAG="pubchem",
    ... )
    >>> validated = validate_config(config)  # doctest: +SKIP
    """
    active_config = ChamanpConfig() if config is None else config
    return _validate_config_impl(active_config)


def run(config: ChamanpConfig | None = None) -> ChamanpResult:
    """Validate and execute CHAMANP, writing configured artifacts to disk.

    Calls ``validate_config`` on *config*, then runs the private pipeline
    implementation. The pipeline curates the molecular dataset, filters by
    target collections, generates Morgan fingerprints, and writes a summary
    report. All artifacts are written to the ``artifacts/`` directory under
    the current working directory.

    Parameters
    ----------
    config : ChamanpConfig, optional
        Runtime configuration. When ``None``, a default ``ChamanpConfig``
        is constructed, validated, and used.

    Returns
    -------
    ChamanpResult
        A frozen result object containing execution status, artifact paths,
        and summary counts. See ``ChamanpResult`` for field descriptions.

    Raises
    ------
    chamanp._core.preflight.ConfigurationError
        If configuration validation fails before execution begins.

    Notes
    -----
    ``run`` creates ``artifacts/`` and ``artifacts/pipeline.log`` in the
    current working directory. Execution failures after preflight raise
    exceptions from the private pipeline internals.

    Examples
    --------
    Run the pipeline with a custom configuration:

    >>> from chamanp import ChamanpConfig, run
    >>> config = ChamanpConfig(
    ...     DATABASE_PATH="data/coconut.csv",
    ...     COLLECTION_TAXONOMY_PATH="data/taxonomy.json",
    ...     TARGET_COLLECTIONS=["PubChem NPs"],
    ...     COLLECTION_TAG="pubchem",
    ... )
    >>> result = run(config)  # doctest: +SKIP
    """
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
