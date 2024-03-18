import barcode
from barcode.writer import ImageWriter
import random
import csv


def calculate_ean13_check_digit(digits):
    """Calculate the EAN-13 check digit for the first 12 digits passed in digits.
    Args:
        digits (str): The first 12 digits of an EAN-13 barcode as a string.
    Returns:
        int: The check digit.
    """
    if len(digits) != 12 or not digits.isdigit():
        raise ValueError("Input must be a string of 12 digits.")

    reversed_digits = digits[::-1]

    odd_sum = sum(int(reversed_digits[i]) for i in range(0, 12, 2))
    even_sum = sum(int(reversed_digits[i]) for i in range(1, 12, 2))

    total = odd_sum * 3 + even_sum
    check_digit = (10 - (total % 10)) % 10

    return str(check_digit)


def generate_unique_ean13_codes(count):
    unique_codes = set()
    while len(unique_codes) < count:
        # Generate a 12-digit random number for EAN-13 (excluding the checksum digit)
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        # Ensure uniqueness
        if random_number not in unique_codes:
            unique_codes.add(random_number)
    return unique_codes

def save_barcode_images(codes):
    CODE_CLASS = barcode.get_barcode_class('ean13-guard')
    with open('dataset/labels/annotations.csv', 'w', newline='') as csvfile:
        fieldnames = ['image_path', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, code in enumerate(codes):
            if i % 100 == 0:
                print(f'Generated {i} barcodes')
            barcode_instance = CODE_CLASS(code, writer=ImageWriter())
            image_path = f'barcode_{i + 1:09}'
            code += calculate_ean13_check_digit(code)
            barcode_instance.save(f'dataset/images/{image_path}')

            writer.writerow({'image_path': image_path + '.png', 'label': code})

number_of_codes = 10000
unique_ean13_codes = generate_unique_ean13_codes(number_of_codes)
save_barcode_images(unique_ean13_codes)

print(f"Finished generating and saving {number_of_codes} unique EAN-13 barcodes.")
