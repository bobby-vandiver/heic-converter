import argparse
import os
from pathlib import Path

import pyheif
from PIL import Image


def convert(heif_filename, output_filename, image_format):
    converted = False
    heif_file = pyheif.read(heif_filename)

    for metadata in heif_file.metadata or []:
        if metadata['type'] == 'Exif':
            output_image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
            output_image.save(output_filename, format=image_format)
            converted = True

    if not converted:
        raise RuntimeError(f"Did not find Exif metadata in {heif_filename}")


def main():
    parser = argparse.ArgumentParser(description='Convert HEIC files')

    parser.add_argument('input',
                        type=str,
                        help='Directory for HEIC files to convert')

    parser.add_argument('output',
                        type=str,
                        help='Directory for converted files')

    parser.add_argument('format',
                        type=str,
                        choices={'png', 'jpeg'},
                        help='Output format')

    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    image_format = args.format

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for subdir, dirs, files in os.walk(input_dir):
        for filename in files:
            input_filename = subdir + os.sep + filename

            if input_filename.endswith('.heic') or input_filename.endswith('.HEIC'):
                output_filename = output_dir + os.sep + os.path.splitext(filename)[0] + '.' + image_format

                try:
                    print(f"[INFO] Converting {input_filename} to {output_filename}")
                    convert(input_filename, output_filename, image_format)
                except Exception as e:
                    print(f"[SKIP] Failed to convert {input_filename}: {e}")


if __name__ == '__main__':
    main()