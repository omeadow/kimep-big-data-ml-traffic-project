from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path


def extract_png_outputs(notebook_path: Path, output_dir: Path) -> list[Path]:
    data = json.loads(notebook_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)

    image_index = 0
    saved: list[Path] = []

    for cell in data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue

        for output in cell.get("outputs", []):
            payload = output.get("data", {})
            png = payload.get("image/png")
            if not png:
                continue

            image_index += 1
            file_path = output_dir / f"junction_{image_index}_actual_vs_pred.png"
            file_path.write_bytes(base64.b64decode(png))
            saved.append(file_path)

    return saved


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract matplotlib PNG outputs from an executed notebook."
    )
    parser.add_argument(
        "--notebook",
        default="notebooks/Untitled.executed.ipynb",
        help="Path to the executed notebook file.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs/figures",
        help="Directory where extracted images will be saved.",
    )

    args = parser.parse_args()
    notebook_path = Path(args.notebook)
    output_dir = Path(args.output_dir)

    if not notebook_path.exists():
        raise FileNotFoundError(
            f"Notebook not found: {notebook_path}. Run notebook execution first."
        )

    saved = extract_png_outputs(notebook_path, output_dir)
    if not saved:
        raise RuntimeError(
            "No PNG images found in notebook outputs. Make sure plot cells were executed."
        )

    print(f"Extracted {len(saved)} plot(s) to {output_dir}")
    for path in saved:
        print(path)


if __name__ == "__main__":
    main()
