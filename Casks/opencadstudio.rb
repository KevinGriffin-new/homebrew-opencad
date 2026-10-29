cask "opencadstudio" do
  # Bumped only by scripts/bump.py, together with opencad-landsurvey: the plugin
  # loads in exactly one host build, so the host must never run ahead of it.
  version "2026.43"
  sha256 "d9a4aa40c5c83852e103a1ef2e9eb711d89fef57582fd195d25588f4649ada0f"

  url "https://github.com/KevinGriffin-new/OpenCADStudio/releases/download/v#{version}-signed/OpenCADStudio-v#{version}-macos-arm64-signed.dmg",
      verified: "github.com/KevinGriffin-new/OpenCADStudio/"
  name "OpenCADStudio"
  desc "Open-source CAD application (Developer ID signed and notarized build)"
  homepage "https://github.com/HakanSeven12/OpenCADStudio"

  livecheck do
    skip "Bumped in lockstep with opencad-landsurvey by scripts/bump.py"
  end

  depends_on arch: :arm64
  depends_on :macos

  app "OpenCADStudio.app"

  # Plugins and settings live here; `brew uninstall --zap` removes them.
  zap trash: "~/Library/Application Support/OpenCADStudio"

  caveats <<~EOS
    This is upstream OpenCADStudio #{version}, built unmodified and signed with
    a Developer ID by KevinGriffin-new. It is not an official upstream build.
  EOS
end
