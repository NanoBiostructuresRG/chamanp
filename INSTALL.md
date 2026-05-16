# CHAMANP Installation And Distribution Notes

CHAMANP is a pre-stable package currently in a stable-release gate cycle. The
current installation goal is to keep the package buildable, installable, and
usable outside the repository checkout while preserving the existing public API
and repository workflow.

Development versions use the PEP 440 `.dev0` format, such as `0.17.0.dev0`.

## Dependency Sources

`pyproject.toml` is the canonical source for package metadata and runtime
dependencies. Runtime dependencies are declared as minimum ranges for users and
downstream packages:

```text
pandas>=1.5
numpy>=1.23.2
rdkit>=2022.9
```

`requirements.txt` is not the canonical package metadata source. It may be kept
as a reproducible local or legacy environment file while CHAMANP is pre-stable.

`environment.yml` describes a conda/mamba environment that can be useful for
local scientific work, especially because RDKit can be sensitive to Python,
platform, and installer channel combinations. Conda/mamba support is helpful,
but it does not replace the pip/PyPI readiness goal.

## Repository Workflow And Package API

### Repository Workflow

`main.py` and the root-level `config.py` together form the repository-based
execution workflow. This workflow is intended for local use and direct
development runs:

```bash
# Edit config.py for your dataset and collection settings, then:
python main.py
```

`config.py` at the repository root is a plain Python module of uppercase
constants. It is not installed as part of the `chamanp` package when a user
runs `pip install chamanp`, and it is not part of the stable public API
contract.

### Public Package API

The stable public API is:

```python
from chamanp import __version__, ChamanpConfig, validate_config, run, ChamanpResult
```

External users and downstream packages should use the package API rather than
the repository workflow. `Pipeline`, `chamanp._core`, and `chamanp._utils` are
private implementation details and are not part of the stable public contract.

## TestPyPI And PyPI

TestPyPI may be used to validate publication mechanics and dependency
resolution before an official release. It is a testing index, not the official
user installation channel. A future stable publication should be validated
against the official PyPI package state separately from any TestPyPI upload.

## Editable Install

Use an editable install while developing from a repository checkout:

```bash
python -m pip install -e .
```

Then verify the installed package doorway:

```bash
python -m chamanp.cli --version
python -m chamanp.cli --help
```

## Build Local Distributions

Build a source distribution and wheel from the repository root:

```bash
python -m build --no-isolation
```

The local build should produce files similar to:

```text
dist/chamanp-<version>.tar.gz
dist/chamanp-<version>-py3-none-any.whl
```

`examples/chamanp.toml` is included in the source distribution. Wheels do not
currently install example profiles as package resources. Users installing from a
wheel should create their own TOML profile or copy the reference profile from
the repository or source distribution.

## Install From A Local Wheel

Install the generated wheel into a clean environment from outside the repository
checkout:

```bash
python -m pip install dist/<wheel>.whl
```

For structure-only smoke tests that should not resolve dependencies from the
network, install the wheel with:

```bash
python -m pip install --no-deps dist/<wheel>.whl
```

The no-deps smoke path is useful for verifying packaging metadata, console
script wiring, and import-safety. It is not a full dependency-resolution test.

## Install From A Local Source Distribution

Install the generated source distribution:

```bash
python -m pip install dist/<sdist>.tar.gz
```

This exercises the source distribution packaging path. It may require build
dependencies and runtime dependencies to be resolvable in the active
environment.

## Local Wheel Smoke Test

CHAMANP includes a PowerShell smoke script for local wheel installation checks:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/smoke_install_wheel.ps1
```

The script builds local distributions, creates a temporary virtual environment
outside the repository checkout, installs the generated wheel, and checks:

- `chamanp --version`
- `chamanp --help`
- public package imports:
  `ChamanpConfig`, `ChamanpResult`, `validate_config`, and `run`
- `Pipeline` remains absent from the public `chamanp` namespace

The default smoke test installs the wheel with `--no-deps` to avoid network
access and keep the check deterministic in restricted environments. Use it as a
packaging and entrypoint smoke test, not as proof that all runtime dependencies
resolve on every platform.

## Continuous Integration

The versioned GitHub Actions workflow validates tests, package build metadata,
`twine check`, and a clean wheel smoke install without running the real pipeline
or regenerating scientific artifacts.

## Out Of Scope For The Smoke Test

The install smoke test does not run the real CHAMANP pipeline, does not generate
project artifacts or reports, and does not validate chemical processing output.
Those behaviors remain covered by focused tests and explicit pipeline
validation workflows.

## Stable Publication Checklist

Follow these steps in order when preparing an official stable release to the
PyPI production index. Do not skip steps and do not publish to PyPI before
completing the full checklist.

### 1. Verify A Clean Main Branch

```bash
git checkout main
git status --short --branch
git log --oneline -5
```

The working tree must be clean and aligned with `origin/main`. Confirm the tip
commit is the intended release commit.

### 2. Run Tests

```bash
python -m pytest tests -p no:cacheprovider --basetemp .pytest_tmp
```

All tests must pass. Remove the temporary directory after:

```powershell
Remove-Item -Recurse -Force .pytest_tmp
```

### 3. Import And API Smoke-Check

```bash
python -m chamanp.cli --version
python -c "import chamanp; print(chamanp.__version__, chamanp.__all__, hasattr(chamanp, 'Pipeline'))"
```

Confirm that the version string matches the intended release version, that
`Pipeline` is absent (`False`), and that `__all__` contains exactly:

```python
['__version__', 'ChamanpConfig', 'validate_config', 'run', 'ChamanpResult']
```

### 4. Build Distributions

```bash
python -m build --no-isolation
```

Confirm both outputs are produced:

```text
dist/chamanp-<version>.tar.gz
dist/chamanp-<version>-py3-none-any.whl
```

### 5. Check Distributions With Twine

```bash
python -m twine check dist/*
```

Both the wheel and the source distribution must pass. Fix any failures before
proceeding.

### 6. Wheel Install Smoke In An Isolated Environment

Install the wheel into a temporary virtual environment created outside the
repository checkout, so the installed package is resolved from the wheel rather
than the local source tree:

```bash
python -m venv .release_venv
.release_venv/bin/python -m pip install dist/chamanp-<version>-py3-none-any.whl
.release_venv/bin/chamanp --version
.release_venv/bin/python -c "import chamanp; print(chamanp.__version__, chamanp.__all__, hasattr(chamanp, 'Pipeline'))"
```

Remove the venv after the check. On Windows, use `.release_venv\Scripts\` instead
of `.release_venv/bin/`.

### 7. Verify The PyPI Package Name

Before the first stable publication, confirm that `chamanp` is available or
already registered under the correct owner on the official PyPI index:

```
https://pypi.org/project/chamanp/
```

If the name is registered by another owner, resolve the conflict before
publishing.

### 8. TestPyPI Versus PyPI

**TestPyPI** (`https://test.pypi.org`) is a validation index only. Uploading to
TestPyPI validates publication mechanics and metadata, but does not constitute
an official release and is not reachable through the normal `pip install chamanp`
path.

**PyPI** (`https://pypi.org`) is the official user-facing index. Publication to
PyPI is the stable release event.

Complete TestPyPI validation before publishing to PyPI. Do not substitute
TestPyPI publication for a PyPI release.

### 9. Publication Method

**Trusted Publishing (preferred).** Configure a Trusted Publisher on PyPI for
the `chamanp` project. Trusted Publishing uses GitHub Actions OIDC tokens,
eliminates the need for long-lived API tokens, and is the recommended path. Set
up a publication workflow that triggers on a version tag push and uploads to
PyPI automatically.

**Manual token upload (explicit fallback only).** If Trusted Publishing is not
configured, generate a scoped API token for the `chamanp` project on PyPI and
upload with:

```bash
python -m twine upload dist/*
```

Use the manual token path only as an explicit, documented fallback. Do not
commit API tokens to the repository or to any tracked environment file.

### 10. Create The Release Tag

After all checks pass and before publishing to PyPI:

```bash
git tag -a v<version> -m "Release v<version>"
git push origin v<version>
```

Use annotated tags (`-a`) for all releases. Confirm the tag points to the
correct commit on `main`.

### 11. Create The GitHub Release

Create a GitHub Release from the tag:

```bash
gh release create v<version> \
  --title "CHAMANP v<version>" \
  --notes-file <release_notes_file>
```

Mark the release as **pre-release** while CHAMANP is in pre-stable development.
Remove the pre-release mark only when declaring a stable public contract. Do not
mark a release as stable before the public API is confirmed frozen.

### 12. Zenodo And DOI

If Zenodo DOI archiving is configured, Zenodo harvests GitHub Releases
automatically when the repository is linked and mints a DOI per release.

Confirm Zenodo record metadata before publishing the GitHub Release, because DOI
records are permanent and cannot be deleted.

CHAMANP does not currently have a Zenodo record or DOI. Skip this step until
Zenodo integration is explicitly configured.

### 13. Rollback And Yank

PyPI does not support deletion of published releases. If a release contains a
critical error:

- Yank the release through the PyPI project management interface. A yanked
  release is excluded from default `pip install` resolution but remains
  installable by explicit version pin.
- Document the yanked release and the reason in `CHANGELOG.md`.
- Publish a corrected release with an incremented version.

Yanking is not a full rollback. Users who installed the affected version before
the yank retain it.

### 14. Artifacts And Reports

Do not regenerate scientific artifacts, pipeline reports, fingerprint matrices,
curated datasets, or any other pipeline output as part of the release process.
The release process covers only distribution packaging and metadata.

Generated outputs live under `artifacts/` and are excluded from the repository
by `.gitignore`. They are never part of a release.
