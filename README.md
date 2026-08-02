# Kodi Build 26

A shareable package of the "Kodi Build 26" setup — includes the full addon collection, userdata (skin settings, sources, favourites, profiles), background media, and additional media assets.

## What's in this repo

Because GitHub blocks individual files over 100 MB, the two largest packages (`addons.zip` and `userdata.zip`) are split into smaller chunks that need to be joined back together before use. `Background.zip` and `media.zip` are small enough to use as-is.

| Folder/File | Contents | Full size |
|---|---|---|
| `build/addons_parts/` | Split chunks of `addons.zip` — all installed Kodi addons (video/audio plugins, repositories, scrapers, modules) | ~183 MB |
| `build/userdata_parts/` | Split chunks of `userdata.zip` — Kodi profile: sources, favourites, guisettings, keymaps, playlists, addon_data, library | ~114 MB |
| `build/Background.zip` | Custom background/wallpaper assets | ~2 MB |
| `build/media.zip` | Additional media assets | ~3 MB |

## Installation instructions

1. Install [Kodi](https://kodi.tv/download) if you haven't already, and launch it once so it creates its default folder structure.
2. Close Kodi completely.
3. Clone or download this repository (use the green **Code → Download ZIP** button on GitHub, or `git clone`).
4. Reassemble the split zip files. From inside the downloaded repo folder, run:

   **macOS/Linux (Terminal):**
   ```sh
   cat build/addons_parts/addons.zip.*.part > addons.zip
   cat build/userdata_parts/userdata.zip.*.part > userdata.zip
   ```

   **Windows (PowerShell):**
   ```powershell
   cmd /c copy /b build\addons_parts\addons.zip.*.part addons.zip
   cmd /c copy /b build\userdata_parts\userdata.zip.*.part userdata.zip
   ```

5. Locate your Kodi "userdata"/config folder for your OS:
   - **Windows:** `%APPDATA%\Kodi\`
   - **macOS:** `~/Library/Application Support/Kodi/`
   - **Linux:** `~/.kodi/`
   - **Android:** `Android/data/org.xbmc.kodi/files/.kodi/`
6. Extract each zip directly into your Kodi folder from step 5, so that:
   - `addons.zip` merges into the `addons/` subfolder
   - `userdata.zip` merges into the `userdata/` subfolder
   - `build/Background.zip` merges into the `Background/` subfolder
   - `build/media.zip` merges into the `media/` subfolder
7. When prompted to overwrite existing files, choose **Yes/Replace All**.
8. Launch Kodi. The build's addons, skin settings, and sources will now be active.

## Verifying the reassembled files (optional)

To confirm nothing got corrupted during download/reassembly, compare checksums:

| File | SHA-256 |
|---|---|
| `addons.zip` | `6f7e9d664594863e6acafb722774dbff5c9bb0b32460c3dae7113898aa1301db` |
| `userdata.zip` | `0a193c42cb93cba28dafd8841a6e5c5bf06b7cc6c203089370864c8dea766939` |

## Notes

- This is a personal build snapshot — some third-party addons/scrapers may need re-configuring depending on your region or may stop working over time as their sources change.
- If antivirus/browser flags the zip as suspicious, this is common for Kodi build files due to the third-party addon scrapers included — the files are as extracted directly from a working Kodi installation.
- Back up your existing Kodi userdata/addons folders before overwriting if you want to preserve your current setup.
