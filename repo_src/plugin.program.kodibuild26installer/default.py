# -*- coding: utf-8 -*-
"""
Kodi Build 26 Installer
Downloads the split build archives from GitHub, reassembles them, and
extracts addons / userdata / Background / media directly into the Kodi
home folder (special://home/).
"""
import os
import json
import shutil
import zipfile
import urllib.request

import xbmc
import xbmcgui
import xbmcvfs

BASE_RAW = "https://raw.githubusercontent.com/Visualfx100/kodi-build-26/main"
HOME = xbmcvfs.translatePath("special://home/")
TEMP = xbmcvfs.translatePath("special://temp/")
ADDON_NAME = "Kodi Build 26 Installer"


def log(msg):
    xbmc.log("[kodibuild26installer] {}".format(msg), xbmc.LOGINFO)


def download(url, dest_path, progress=None, label=""):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Kodi)"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        total = int(resp.headers.get("Content-Length", 0) or 0)
        downloaded = 0
        chunk_size = 256 * 1024
        with open(dest_path, "wb") as f:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if progress is not None:
                    if progress.iscanceled():
                        raise RuntimeError("Installation cancelled by user")
                    if total:
                        pct = min(99, int(downloaded * 100 / total))
                        progress.update(pct, label)


def build_zip_from_parts(work_dir, part_names, repo_subdir, out_name, progress, label):
    out_path = os.path.join(work_dir, out_name)
    with open(out_path, "wb") as out_f:
        for i, part in enumerate(part_names):
            part_url = "{}/{}/{}".format(BASE_RAW, repo_subdir, part)
            part_path = os.path.join(work_dir, part)
            step_label = "{} ({}/{})".format(label, i + 1, len(part_names))
            download(part_url, part_path, progress, step_label)
            with open(part_path, "rb") as pf:
                shutil.copyfileobj(pf, out_f)
            os.remove(part_path)
    return out_path


def extract_zip(zip_path, dest_dir, progress, label):
    progress.update(99, "Extracting {}...".format(label))
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(dest_dir)


def main():
    dialog = xbmcgui.Dialog()
    proceed = dialog.yesno(
        ADDON_NAME,
        "This will download and install the Kodi Build 26 addon pack.\n\n"
        "It will overwrite matching files in your addons, userdata, Background, "
        "and media folders. Continue?",
    )
    if not proceed:
        return

    work_dir = os.path.join(TEMP, "kodibuild26_install")
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir, ignore_errors=True)
    os.makedirs(work_dir)

    progress = xbmcgui.DialogProgress()
    progress.create(ADDON_NAME, "Fetching build manifest...")

    try:
        manifest_path = os.path.join(work_dir, "manifest.json")
        download(BASE_RAW + "/manifest.json", manifest_path, progress, "Fetching manifest...")
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        # Addons
        addons_zip = build_zip_from_parts(
            work_dir, manifest["addons_parts"], "build/addons_parts",
            "addons.zip", progress, "Downloading addons",
        )
        extract_zip(addons_zip, HOME, progress, "addons")
        os.remove(addons_zip)

        # Userdata
        userdata_zip = build_zip_from_parts(
            work_dir, manifest["userdata_parts"], "build/userdata_parts",
            "userdata.zip", progress, "Downloading userdata",
        )
        extract_zip(userdata_zip, HOME, progress, "userdata")
        os.remove(userdata_zip)

        # Background
        bg_path = os.path.join(work_dir, manifest["background"])
        download(BASE_RAW + "/build/" + manifest["background"], bg_path, progress, "Downloading Background")
        extract_zip(bg_path, HOME, progress, "Background")
        os.remove(bg_path)

        # Media
        media_path = os.path.join(work_dir, manifest["media"])
        download(BASE_RAW + "/build/" + manifest["media"], media_path, progress, "Downloading media")
        extract_zip(media_path, HOME, progress, "media")
        os.remove(media_path)

        progress.close()
        shutil.rmtree(work_dir, ignore_errors=True)

        dialog.ok(
            ADDON_NAME,
            "Installation complete.\n\nPlease restart Kodi now to load the new "
            "addons, skin settings, and sources.",
        )
        log("Installation completed successfully")

    except Exception as exc:
        progress.close()
        shutil.rmtree(work_dir, ignore_errors=True)
        log("Installation failed: {}".format(exc))
        dialog.ok(ADDON_NAME, "Installation failed:\n\n{}".format(str(exc)))


if __name__ == "__main__":
    main()
