# Kodi Build 26

A shareable package of the "Kodi Build 26" setup — includes the full addon collection, userdata (skin settings, sources, favourites, profiles), background media, and additional media assets.

## What's in the release

The actual build files are attached to the [Releases](../../releases) page of this repository (too large for regular Git storage):

| File | Contents | Approx. size |
|---|---|---|
| `addons.zip` | All installed Kodi addons (video/audio plugins, repositories, scrapers, modules) | ~183 MB |
| `userdata.zip` | Kodi profile: sources, favourites, guisettings, keymaps, playlists, addon_data, library | ~114 MB |
| `Background.zip` | Custom background/wallpaper assets | ~2 MB |
| `media.zip` | Additional media assets | ~3 MB |

## Installation instructions

1. Install [Kodi](https://kodi.tv/download) if you haven't already, and launch it once so it creates its default folder structure.
2. Close Kodi completely.
3. Locate your Kodi "userdata" folder for your OS:
   - **Windows:** `%APPDATA%\Kodi\`
   - **macOS:** `~/Library/Application Support/Kodi/`
   - **Linux:** `~/.kodi/`
   - **Android:** `Android/data/org.xbmc.kodi/files/.kodi/`
4. Download `addons.zip`, `userdata.zip`, `Background.zip`, and `media.zip` from the [latest release](../../releases/latest).
5. Extract each zip directly into your Kodi folder from step 3, so that:
   - `addons.zip` merges into the `addons/` subfolder
   - `userdata.zip` merges into the `userdata/` subfolder
   - `Background.zip` merges into the `Background/` subfolder
   - `media.zip` merges into the `media/` subfolder
6. When prompted to overwrite existing files, choose **Yes/Replace All**.
7. Launch Kodi. The build's addons, skin settings, and sources will now be active.

## Notes

- This is a personal build snapshot — some third-party addons/scrapers may need re-configuring depending on your region or may stop working over time as their sources change.
- If antivirus/browser flags the zip as suspicious, this is common for Kodi build files due to the third-party addon scrapers included — the files are as extracted directly from a working Kodi installation.
- Back up your existing Kodi userdata/addons folders before overwriting if you want to preserve your current setup.
