import re
import subprocess
import sys

import Levenshtein


def get_license_plate(image_path: str, real_string: str) -> dict:
    """
    The get_license_plate function takes an image path and a real string as arguments.
    It then uses the OpenALPR command line tool to extract the license plate from the image.
    The function returns a dictionary containing both the extracted license plate text and 
    the similarity score between that text and the real string.
    
    :param image_path: str: Specify the path to the image file
    :param real_string: str: Compare the captured license plate string to a real one
    :return: A dictionary with the license plate number and the similarity score
    """
    if sys.platform == 'linux':
        result = subprocess.run(
            [
                "wine64",
                "alpr",
                "--country",
                "us",
                "--config",
                "openalpr.conf",
                image_path,
            ],
            capture_output=True,
            text=True,
        )
    else:
        result = subprocess.run(
            [
                "alpr",
                "--country",
                "us",
                "--config",
                "openalpr.conf",
                image_path,
            ],
            capture_output=True,
            text=True,
        )

    # Get first line of output
    output_lines = result.stdout.splitlines()
    try:
        if output_lines:
            first_line = output_lines[1].strip()
            match = re.search(r"-\s+([A-Z0-9]+)\s+", first_line)
            if match:
                text = match.group(1)
            else:
                print("None")
        else:
            print("No output from command.")
    except IndexError:
        print("No license plates found.")

    try:
        captured_string = text

        # Compute Levenshtein distance
        distance = Levenshtein.distance(captured_string, real_string)

        # Compute similarity as a ratio of the distance to the length of the longer string
        similarity = 1 - distance / max(len(captured_string), len(real_string))

    except NameError:
        text = None
        similarity = None
        print("No similarity found.")
        
    return {"License Plate":text, "Similarity Score":similarity}

plate = get_license_plate(image_path="plate0.jpg", real_string="XB127SKK")
plate_text = plate.get("License Plate")
print(plate)
print(plate_text)
