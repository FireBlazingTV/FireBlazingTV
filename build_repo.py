#!/usr/bin/env python3
"""Packages repo_src/* addons into repo/zips/*, and generates repo/addons.xml + md5."""
import os
import shutil
import zipfile
import hashlib
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "repo_src")
REPO = os.path.join(ROOT, "repo")
ZIPS = os.path.join(REPO, "zips")

ADDONS = [
    ("repository.fireblazingtv", "1.0.0"),
    ("plugin.program.fireblazingtvinstaller", "1.0.0"),
]


def write_index_html(dir_path, filenames):
    """Writes a plain HTML directory listing so Kodi's HTTP file browser
    (which needs <a href> links, not GitHub's normal 404-on-folder behavior)
    can list files when this folder is served as a static site (GitHub Pages)."""
    links = "\n".join(
        '<li><a href="{name}">{name}</a></li>'.format(name=name) for name in filenames
    )
    html = (
        "<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>\n"
        "<ul>\n{links}\n</ul>\n</body></html>\n"
    ).format(links=links)
    with open(os.path.join(dir_path, "index.html"), "w") as f:
        f.write(html)


def zip_addon(addon_id, version):
    src_dir = os.path.join(SRC, addon_id)
    out_dir = os.path.join(ZIPS, addon_id)
    os.makedirs(out_dir, exist_ok=True)
    zip_name = "{}-{}.zip".format(addon_id, version)
    zip_path = os.path.join(out_dir, zip_name)
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, _, filenames in os.walk(src_dir):
            for fn in filenames:
                fp = os.path.join(dirpath, fn)
                arcname = os.path.join(addon_id, os.path.relpath(fp, src_dir))
                zf.write(fp, arcname)
    # Also drop a copy of addon.xml and icon.png alongside the zip (standard repo layout)
    for extra in ("addon.xml", "icon.png"):
        src_extra = os.path.join(src_dir, extra)
        if os.path.exists(src_extra):
            shutil.copy2(src_extra, os.path.join(out_dir, extra))
    write_index_html(out_dir, [zip_name, "addon.xml", "icon.png"])
    print("Packaged", zip_path)
    return zip_path


def build_addons_xml():
    root = ET.Element("addons")
    for addon_id, version in ADDONS:
        addon_xml_path = os.path.join(SRC, addon_id, "addon.xml")
        tree = ET.parse(addon_xml_path)
        root.append(tree.getroot())
    os.makedirs(REPO, exist_ok=True)
    addons_xml_path = os.path.join(REPO, "addons.xml")
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(addons_xml_path, encoding="UTF-8", xml_declaration=True)
    print("Wrote", addons_xml_path)
    return addons_xml_path


def write_md5(addons_xml_path):
    with open(addons_xml_path, "rb") as f:
        data = f.read()
    digest = hashlib.md5(data).hexdigest()
    md5_path = addons_xml_path + ".md5"
    with open(md5_path, "w") as f:
        f.write(digest)
    print("Wrote", md5_path, "=", digest)


def main():
    if os.path.exists(ZIPS):
        shutil.rmtree(ZIPS)
    for addon_id, version in ADDONS:
        zip_addon(addon_id, version)
    addons_xml_path = build_addons_xml()
    write_md5(addons_xml_path)
    # Top-level zips/ index so Kodi can browse into each addon folder
    write_index_html(ZIPS, [addon_id + "/" for addon_id, _ in ADDONS])
    # .nojekyll so GitHub Pages serves these files/folders as-is
    with open(os.path.join(ROOT, ".nojekyll"), "w") as f:
        f.write("")


if __name__ == "__main__":
    main()
