# Sortphotos

Sortphotos is a very simple command-line tool designed to help you organize your photo collection. It automatically sorts photos into directories based on their metadata, such as the date they were taken. This makes it easier to manage and find your photos, ensuring that your memories are well-organized and easily accessible.

## Features

- **Automatic Sorting**: Sorts photos into directories by date.
- **Metadata Extraction**: Uses photo metadata to determine the correct sorting order.
- **Customizable**: Allows customization of directory structure and naming conventions.
- **Support for Various Formats**: Works with multiple photo formats including JPEG, CR2, and more.

## Usage

To use Sortphotos, simply run the following command in your terminal:

```sh
python sortphotos.py /path/to/source /path/to/destination
```
Replace `/path/to/source` with the directory containing your photos and `/path/to/destination` with the directory where you want the sorted photos to be placed. The `--pattern` option allows you to specify the directory structure, for example:

```sh
$ ls PhotoLibrary
IMG_0419.CR2
$ python sortphotos.py PhotoLibrary --pattern "%Y-%m-%d-%original_filename"
Moved PhotoLibrary/IMG_0419.CR2 to PhotoLibrary/2024-04-17-IMG_0419.CR2
```

Note the default pattern is: `%Y/%m/%d/%original_filename`. For more options, use `--help`.

## Why??

I used to used Lightroom, but then I did not use it often enough to justify paying the subscriptions and I switched to something else. I could try Adobe Bridge, but I think it is very heavy for what I want. Yet, I liked organizing the files using a given pattern. I found out about a project called [elodie](https://github.com/jmathai/elodie) that suited my needs, but it seems kind of abandoned now, so I just wrote this one that suits my needs. If you like it, add a star, I will appreciate it 😊.

## License

Sortphotos is licensed under the Apache License 2.0.
