# homebrew-opencad

Homebrew casks for [OpenCADStudio](https://github.com/HakanSeven12/OpenCADStudio)
and the [Land Survey plugin](https://github.com/KevinGriffin-new/opencad-landsurvey-plugin).
Apple Silicon only.

```sh
brew tap kevingriffin-new/opencad
brew install --cask opencad-landsurvey   # installs OpenCADStudio too
```

| cask | installs |
|---|---|
| `opencadstudio` | `OpenCADStudio.app`: upstream's release built unmodified, Developer ID signed and notarized. Not an official upstream build. |
| `opencad-landsurvey` | the plugin, into `~/Library/Application Support/OpenCADStudio/plugins/opencad.landsurvey` |

## Versions move together

The plugin loads in exactly one OpenCADStudio build. Homebrew can't express
"depends on opencadstudio version X", so this tap never bumps the host on its
own: `scripts/bump.py` reads the host version from the plugin release's build
metadata and moves both casks in the same commit. `brew upgrade` therefore
never leaves you with a host the plugin refuses.

The trade-off: a new OpenCADStudio release reaches this tap only after the
plugin has been re-pinned to it, which is usually within hours.

## Already installed by hand?

- App already in `/Applications`: `brew install --cask --adopt opencadstudio`
- Plugin already installed from the Plugin Manager: remove
  `~/Library/Application Support/OpenCADStudio/plugins/opencad.landsurvey`
  first, or `brew install --cask --force opencad-landsurvey`.

If you later update the plugin from the Plugin Manager, Homebrew's record
goes stale. `brew reinstall --cask opencad-landsurvey` resyncs it.

## Maintaining

`.github/workflows/bump.yml` runs every three hours and on demand:

```sh
gh workflow run bump.yml -R KevinGriffin-new/homebrew-opencad
```

If the plugin targets a host whose signed build isn't published yet, the run
waits (exit 3) and tries again next time. Any other failure opens a
"bump failing" issue.
