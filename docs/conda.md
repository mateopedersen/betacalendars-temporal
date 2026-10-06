# Conda package

The public package is distributed from the Beta Calendars Anaconda.org channel as `betacalendars-temporal`. Install it with:

```sh
conda install betacalendars::betacalendars-temporal
```

The Conda recipe is in `conda-recipe/meta.yaml`. The package is `noarch: python`, uses Python 3.11 or later, and has no runtime dependencies beyond Python.

For a local release build, keep Conda auto-upload disabled. Build the recipe, then run `python scripts/sanitize_conda_artifact.py PATH_TO_PACKAGE.conda` on the generated archive. This removes pip's source-location record and build-machine bytecode and paths from the published artifact. Install and exercise that exact sanitized file in a fresh environment before uploading it to Anaconda.org's `test` label; only promote the tested file to `main`.
