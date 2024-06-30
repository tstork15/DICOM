import pydicom


def parse_dicom(file_path):
    """
    Parse the DICOM file and extract the tags and their values.

    Parameters:
    file_path (str): The path to the DICOM file.

    Returns:
    dicom_data (list): A list of tuples containing tag information (tag number, tag name, VR, and value).
    """
    dicom_file = pydicom.dcmread(file_path)  # Read the file with Pydicom
    dicom_data = []  # Initialize an empty list to store the parsed DICOM tag data

    def process_element(elem, indent=""):
        """
        Recursively process each element in the DICOM file.

        Parameters:
        elem: The DICOM element to process.
        indent (str): The indentation for nested elements.

        Outputs:
        None (modifies the global dicom_data list)
        """
        tag_num = elem.tag  # Get the tag number of the DICOM element (e.g., (0010,0020))
        tag_name = pydicom.datadict.keyword_for_tag(tag_num)  # Get the keyword for the tag number (e.g., Patient ID)
        if not tag_name:
            tag_name = 'Unknown'  # If the tag name is not found (e.g., private tags), set it to 'Unknown'
        value = elem.value  # Get the value (aka the actual data stored) of the DICOM element

        # Handle multi-line text by replacing \r\n with commas for better readability
        if isinstance(value, str):
            value = value.replace('\r\n', ', ')

        # Sequence (VR = SQ) handling
        if elem.VR == 'SQ':  # Check if the Value Representation (VR) is a Sequence (SQ)
            # Add the sequence tag information to the list, stating the number of items in the sequence
            dicom_data.append((f"{indent}{tag_num}", tag_name, elem.VR, f"Sequence of {len(value)} items"))
            for item in value:  # Iterate over each item in the sequence
                for seq_elem in item:  # Iterate over each element in the sequence item
                    # Recursively process each element in the sequence item with increased indentation
                    process_element(seq_elem, indent + "  ")
        else:  # If the element is not a sequence
            # Add the element's tag information to the list
            dicom_data.append((f"{indent}{tag_num}", tag_name, elem.VR, value))

    # Process each element in the DICOM file
    for elem in dicom_file:
        process_element(elem)

    return dicom_data


if __name__ == "__main__":
    print("Do not run this file directly!")
