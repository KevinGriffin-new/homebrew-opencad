cask "opencad-landsurvey" do
  version "0.4.27"
  sha256 "e573827ea6091cf295fb3587bfd9ea0321caf812810577774710f1d48e5c24c1"

  url "https://github.com/KevinGriffin-new/opencad-landsurvey-plugin/releases/download/v#{version}/opencad.landsurvey-macos-aarch64.tar.gz"
  name "Land Survey for OpenCADStudio"
  desc "Survey points, COGO, TIN surfaces and field-to-finish for OpenCADStudio"
  homepage "https://github.com/KevinGriffin-new/opencad-landsurvey-plugin"

  livecheck do
    skip "Bumped in lockstep with opencadstudio by scripts/bump.py"
  end

  depends_on arch: :arm64
  depends_on cask: "kevingriffin-new/opencad/opencadstudio"

  # The tarball unpacks to opencad.landsurvey/{*.dylib, plugin.toml}, the layout
  # the host discovers in its per-user plugins directory.
  artifact "opencad.landsurvey",
           target: "~/Library/Application Support/OpenCADStudio/plugins/opencad.landsurvey"

  caveats <<~EOS
    Built for OpenCADStudio 2026.44 exactly; other host versions refuse it.
    Upgrade both together with `brew upgrade --cask opencad-landsurvey`.

    If you also update the plugin from OpenCADStudio's Plugin Manager, Homebrew
    no longer tracks what is installed; reinstall the cask to resync.
  EOS
end
