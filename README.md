# DICOM Tag Viewer
![dicom-tag-viewer](https://github.com/tstork15/dicom-tag-viewer/assets/43816229/00ae098e-fb4a-4434-879f-c49de8df4800)

## Overview
The DICOM Tag Viewer is a utility for viewing the tags of DICOM files. It provides a graphical user interface (GUI) using `tkinter` to select and display DICOM files, and it allows users to filter tags based on a search query. This tool is useful for medical imaging professionals and developers working with DICOM files.

## Features
- **File Selection**: Easily select a DICOM file from a directory using the GUI.
- **Preload Additional Files**: Additional DICOM files in the same directory (e.g., CT slices) will be loaded into a menu to facilitate easy switching between files.
- **Tag Display**: View DICOM tags, including nested sequences, in a structured Treeview format.
- **Search Functionality**: Filter displayed tags based on a search query. Searches will stay active while files are switched using the GUI menu but reset when selecting a new source file.
- **Alternating Row Colors**: Improved readability with alternating row colors.
- **Auto-adjusting Column Widths**: Columns automatically adjust their width based on the content.

## Requirements
- Python 3.x
- pydicom

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/tstork15/dicom-tag-viewer.git
    cd dicom-tag-viewer
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the `dicomTagViewer.py` script:
    ```bash
    python dicomTagViewer.py
    ```
2. Use the "Select DICOM File" button to open a file dialog and select a DICOM file.
3. View the DICOM tags in the Treeview.
4. Use the search box to filter tags based on your query.
5. Switch to another file in the same directory (e.g., CT slices)
