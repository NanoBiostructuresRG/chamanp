# CHAMANP Installation And Distribution Notes

CHAMANP is a pre-stable package. The current installation goal is to make the
package buildable, installable, and usable outside the repository checkout while
preserving the existing public API and repository workflow.

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
currently install example profiles as package resources.

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

## Out Of Scope For The Smoke Test

The install smoke test does not run the real CHAMANP pipeline, does not generate
project artifacts or reports, and does not validate chemical processing output.
Those behaviors remain covered by focused tests and explicit pipeline
validation workflows.
