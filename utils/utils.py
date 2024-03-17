import os
import shutil


def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory, exist_ok=True)


def copy_files(source_directory, destination_directory):
    """
    Copies the files from source_directory to destination_directory. Overwrites any existing files
    in destination_directory with their source_directory counterparts. Does not copy subdirectories.

    :param source_directory: Source directory from which to copy files.
    :param destination_directory: Destination directory to which to copy files.
    """
    if not os.path.exists(source_directory):
        raise ValueError(f"Source directory does not exist: {source_directory}")

    os.makedirs(destination_directory, exist_ok=True)

    for item in os.listdir(source_directory):
        src_path = os.path.join(source_directory, item)
        dest_path = os.path.join(destination_directory, item)

        if os.path.isfile(src_path):
            shutil.copy2(src_path, dest_path)
