from datetime import datetime
import os
import sys

import typer
from PIL import Image
from PIL.ExifTags import TAGS

app = typer.Typer()


def get_exif_data(image_path: str):
    """
    Extracts EXIF data from an image file.

    Args:
        image_path (str): The path to the image file.

    Returns:
        dict: A dictionary containing the EXIF data tags and their corresponding values.
              If no EXIF data is found or an error occurs, an empty dictionary is returned.

    Raises:
        Exception: If there is an error reading the EXIF data from the image file.
    """
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        if exif_data is not None:
            return {TAGS.get(tag): value for tag, value in exif_data.items()}
    except Exception as e:
        typer.echo(f"Error reading EXIF data from {image_path}: {e}", err=True)
    return {}


def get_photos_with_dates(path: str):
    """
    Retrieves photos along with their dates from the specified directory.

    This function walks through the given directory, extracts EXIF data from each photo,
    and retrieves the date and time when the photo was taken. If the EXIF data does not
    contain a date, the photo is skipped.

    Args:
        path (str): The path to the directory containing the photos.

    Returns:
        dict: A dictionary where the keys are photo filenames and the values are datetime objects
              representing when the photos were taken. If the path does not exist, an empty dictionary
              is returned.
    """
    if not os.path.exists(path):
        typer.echo(f"Path {path} does not exist.")
        return {}

    photos_with_dates = {}
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            exif_data = get_exif_data(file_path)
            date_time = exif_data.get("DateTime")
            if date_time:
                date_time = datetime.strptime(date_time, "%Y:%m:%d %H:%M:%S")
                photos_with_dates[file] = date_time
            else:
                typer.echo(
                    f"No date found in EXIF data for {file_path}, skipping it", err=True
                )

    return photos_with_dates


def move_and_rename_photo(
    origin_path: str,
    destination_path: str,
    filename: str,
    date_time: datetime,
    pattern: str,
    dry_run: bool = False,
) -> None:
    """
    Move and rename a photo based on the given date and pattern.

    Args:
        origin_path (str): The root directory where the photo is located.
        destination_path (str): The destination directory where the photo will be moved.
        filename (str): The name of the photo file.
        date_time (datetime): The date and time to use for renaming.
        pattern (str): The pattern to use for the new file path.
        dry_run (bool, optional): If True, only print the actions without performing them. Defaults to False.
    """
    # Generate the new path based on the date and pattern. Note the % in %original_filename will be removed by strftime
    new_path = date_time.strftime(pattern).replace("original_filename", filename)
    full_new_path = os.path.join(destination_path, new_path)
    if dry_run:
        # If dry run, just print what would be done
        typer.echo(
            f"Dry run would move {os.path.join(origin_path, filename)} to {full_new_path}"
        )
        return

    os.makedirs(os.path.dirname(full_new_path), exist_ok=True)
    old_file_path = os.path.join(origin_path, filename)
    os.rename(old_file_path, full_new_path)
    typer.echo(f"Moved {old_file_path} to {full_new_path}")


@app.command()
def sortphotos(
    origin_path: str,
    destination_path: str = None,
    pattern: str = "%Y/%m/%d/%original_filename",
    dry_run: bool = False,
):
    """
    Sort photos by date.

    Args:
        origin_path (str): The root directory where the photos are located.
        destination_path (str, optional): The destination directory where the photos will be moved.
            If not set, the origin_path will be used.
        pattern (str, optional): The pattern to use for the new file path. Defaults to "%Y/%m/%d/%original_filename".
        dry_run (bool, optional): If True, only print the actions without performing them. Defaults to False.
    """
    if destination_path is None:
        destination_path = origin_path
    photos_with_dates = get_photos_with_dates(origin_path)

    for photo, date in photos_with_dates.items():
        move_and_rename_photo(origin_path, destination_path, photo, date, pattern, dry_run)


if __name__ == "__main__":
    sys.exit(app())
