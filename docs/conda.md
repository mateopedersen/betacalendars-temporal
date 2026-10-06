# Conda package

`betacalendars-temporal` is published as a `noarch: python` package in the public Beta Calendars Prefix.dev channel. Python 3.11 or later is required; the package has no runtime dependencies beyond Python.

With Pixi:

```sh
pixi add --channel https://prefix.dev/mateopedersen/betacalendars betacalendars-temporal
```

With Conda or Mamba:

```sh
conda install --override-channels \
  -c https://prefix.dev/mateopedersen/betacalendars \
  -c conda-forge \
  betacalendars-temporal
```

The Rattler-Build recipe is [`recipe.yaml`](../recipe.yaml). The release workflow builds and tests that recipe against the immutable GitHub release source, then publishes the package to `mateopedersen/betacalendars` with OIDC and a Sigstore attestation.
