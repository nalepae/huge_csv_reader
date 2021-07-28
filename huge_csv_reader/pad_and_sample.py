from pathlib import Path
from typing import List, Tuple

from huge_csv_reader.pad import pad
from huge_csv_reader.padded_text_file import padded_text_file
from huge_csv_reader.sample import sample, sample_sampled
from huge_csv_reader.pseudo_hash import pseudo_hash


def pad_and_sample(
    source_csv_file_path: Path,
    dest_dir_path: Path,
    x: str,
    ys_and_types: List[Tuple[str, type]],
) -> None:
    """Pad and sample `source_csv_file_path` into `dest_dir_path` with `x`.

    If the file is already sampled, this function does not resample it but exits
    immediately without error.
    """
    dir_path = dest_dir_path / pseudo_hash(source_csv_file_path, x)

    try:
        dir_path.mkdir(parents=True)
    except FileExistsError:
        return

    padded_path = dir_path / "0.csv"
    sampled_path = dir_path / "1.csv"

    pad(source_csv_file_path, padded_path)

    with padded_text_file(padded_path, offset=1) as ptf:
        nb_lines = len(ptf)

    if nb_lines > 1:
        sample(source_csv_file_path, sampled_path, x, ys_and_types, period=2)
        pad(sampled_path)

    with padded_text_file(sampled_path, offset=1) as ptf:
        nb_lines = len(ptf)

    epoch = 2

    while nb_lines > 1:
        new_sampled_path = dir_path / f"{epoch}.csv"
        sample_sampled(sampled_path, new_sampled_path, period=2)

        sampled_path = new_sampled_path
        pad(sampled_path)

        with padded_text_file(sampled_path, offset=1) as ptf:
            nb_lines = len(ptf)

        epoch += 1