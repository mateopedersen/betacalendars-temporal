"""Remove build-machine metadata and bytecode from a noarch Conda archive."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _remove_record_entries(record: Path, removed: set[str]) -> None:
    if not record.exists():
        return
    rows = list(csv.reader(io.StringIO(record.read_text(encoding="utf-8"))))
    kept = [row for row in rows if not row or row[0] not in removed]
    output = io.StringIO(newline="")
    csv.writer(output, lineterminator="\n").writerows(kept)
    record.write_text(output.getvalue(), encoding="utf-8")


def sanitize(archive: Path) -> None:
    archive = archive.resolve()
    with tempfile.TemporaryDirectory(prefix="betacal-conda-sanitize-") as temp:
        root = Path(temp) / "package"
        subprocess.run(["cph", "extract", str(archive), "--dest", str(root)], check=True)

        removed: set[str] = set()
        for bytecode in root.rglob("*.pyc"):
            relative = bytecode.relative_to(root).as_posix()
            removed.add(relative)
            bytecode.unlink()
        for cache in sorted(root.rglob("__pycache__"), reverse=True):
            if cache.is_dir():
                cache.rmdir()

        for direct_url in root.glob("site-packages/*.dist-info/direct_url.json"):
            removed.add(direct_url.relative_to(root).as_posix())
            direct_url.unlink()

        site_packages = root / "site-packages"
        removed_records = {
            Path(item).relative_to(site_packages.relative_to(root)).as_posix()
            for item in removed
            if Path(item).is_relative_to(site_packages.relative_to(root))
        }
        for record in root.glob("site-packages/*.dist-info/RECORD"):
            _remove_record_entries(
                record, removed_records | {f"{record.parent.name}/direct_url.json"}
            )

        paths_file = root / "info" / "paths.json"
        if paths_file.exists():
            data = json.loads(paths_file.read_text(encoding="utf-8"))
            data["paths"] = [item for item in data["paths"] if item["_path"] not in removed]
            for item in data["paths"]:
                path = root / item["_path"]
                if item["_path"].endswith(".dist-info/RECORD") and path.exists():
                    contents = path.read_bytes()
                    item["sha256"] = hashlib.sha256(contents).hexdigest()
                    item["size_in_bytes"] = len(contents)
            paths_file.write_text(
                json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )

        files_file = root / "info" / "files"
        if files_file.exists():
            lines = files_file.read_text(encoding="utf-8").splitlines()
            files_file.write_text(
                "".join(f"{line}\n" for line in lines if line not in removed),
                encoding="utf-8",
            )

        absolute = re.compile(r"/(?:Users|private|var/folders)/[^\s'\"]+")
        for metadata in (root / "info" / "recipe").glob("meta.yaml*"):
            if metadata.exists():
                lines = metadata.read_text(encoding="utf-8").splitlines()
                metadata.write_text(
                    "\n".join(line for line in lines if not absolute.search(line)) + "\n",
                    encoding="utf-8",
                )

        output_folder = Path(temp) / "output"
        output_folder.mkdir()
        subprocess.run(
            ["cph", "create", str(root), archive.name, "--out-folder", str(output_folder)],
            check=True,
        )
        shutil.move(output_folder / archive.name, archive)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: sanitize_conda_artifact.py PACKAGE.conda")
    sanitize(Path(sys.argv[1]))
