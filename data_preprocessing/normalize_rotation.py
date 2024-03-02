import pandas as pd
import os
import glob


def modify_csv_with_pandas(file_path, file_number):
    df = pd.read_csv(file_path, sep=r'\s+', header=None)
    df.iloc[0, 0] = file_number % 4
    df.to_csv(file_path, header=False, index=False, sep=' ')


def process_text_files_in_directory(directory_path):
    text_files = sorted(glob.glob(os.path.join(directory_path, '*.txt')))

    for file_number, file_path in enumerate(text_files):
        try:
            modify_csv_with_pandas(file_path, file_number)
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")


if __name__ == "__main__":
    directory_path = '../dataset/labels'
    process_text_files_in_directory(directory_path)
    print("Processing complete.")
