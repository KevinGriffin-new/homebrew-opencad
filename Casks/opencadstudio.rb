cask "opencadstudio" do
  # Bumped only by scripts/bump.py, together with opencad-landsurvey: the plugin
  # loads in exactly one host build, so the host must never run ahead of it.
  version "2026.44"
  sha256 "26939f85a4d7009c269475f2e0a278af7f827d26ee6a5bea355062ac843c53a9"

  url "https://github.com/KevinGriffin-new/OpenCADStudio/releases/download/v#{version}-signed/OpenCADStudio-v#{version}-macos-arm64-signed.dmg"
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
