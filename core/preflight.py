# core/preflight.py

import os
import re


class ConfigurationError(Exception):
    """Raised when CHAMANP configuration fails preflight validation."""


SAFE_COLLECTION_TAG_PATTERN = re.compile(r"^[A-Za-z0-9_-]+$")


def validate_config(config):
    errors = []

    database_path = getattr(config, "DATABASE_PATH", None)
    if not database_path:
        errors.append("DATABASE_PATH is required.")
    elif not os.path.exists(database_path):
        errors.append(f"DATABASE_PATH does not exist: {database_path}")

    taxonomy_path = getattr(config, "COLLECTION_TAXONOMY_PATH", None)
    if not taxonomy_path:
        errors.append("COLLECTION_TAXONOMY_PATH is required.")
    elif not os.path.exists(taxonomy_path):
        errors.append(f"COLLECTION_TAXONOMY_PATH does not exist: {taxonomy_path}")

    target_collections = getattr(config, "TARGET_COLLECTIONS", None)
    if not target_collections:
        errors.append("TARGET_COLLECTIONS is required and must not be empty.")
    elif isinstance(target_collections, str):
        errors.append("TARGET_COLLECTIONS must be a non-empty collection of names, not a string.")

    collection_logic = getattr(config, "COLLECTION_LOGIC", None)
    if not isinstance(collection_logic, str):
        errors.append("COLLECTION_LOGIC must be either 'OR' or 'AND'.")
    else:
        normalized_logic = collection_logic.strip().upper()
        if normalized_logic not in {"OR", "AND"}:
            errors.append("COLLECTION_LOGIC must be either 'OR' or 'AND'.")
        else:
            config.COLLECTION_LOGIC = normalized_logic

    collection_tag = getattr(config, "COLLECTION_TAG", None)
    if not isinstance(collection_tag, str) or not collection_tag.strip():
        errors.append("COLLECTION_TAG is required and must not be empty.")
    else:
        normalized_tag = collection_tag.strip()
        if not SAFE_COLLECTION_TAG_PATTERN.fullmatch(normalized_tag):
            errors.append(
                "COLLECTION_TAG may contain only letters, numbers, underscores, and hyphens."
            )
        else:
            config.COLLECTION_TAG = normalized_tag

    _validate_non_negative_integer(config, "MORGAN_RADIUS", errors)
    _validate_positive_integer(config, "MORGAN_BITS", errors)

    if errors:
        raise ConfigurationError("Configuration preflight failed: " + "; ".join(errors))

    return config


def _validate_non_negative_integer(config, name, errors):
    value = getattr(config, name, None)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        errors.append(f"{name} must be an integer >= 0.")


def _validate_positive_integer(config, name, errors):
    value = getattr(config, name, None)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        errors.append(f"{name} must be a positive integer.")
