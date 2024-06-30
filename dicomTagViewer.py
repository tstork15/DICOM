import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.font as tkFont
import os
from dicomReadHelper import parse_dicom

# Initialize an empty list to store the original data to restore when the search box is cleared
original_data = []

def select_file_and_display_data():
    """
    Open a file dialog to select a DICOM file and display its tags.

    Inputs: None
    Outputs: None
    """
    # Open a file dialog to select a DICOM file and get its path
    file_path = filedialog.askopenfilename(title="Select DICOM file", filetypes=[("DICOM files", "*.dcm")])

    if file_path: # If a file is selected

        # Get the directory of the selected file
        folder_path = os.path.dirname(file_path)

        # List all DICOM files in the directory
        dicom_files = [file for file in os.listdir(folder_path) if file.endswith(".dcm")]

        if dicom_files:
            # If there are DICOM files in the directory

            # Get the name of the selected file
            file_name = os.path.basename(file_path)

            # Update the file selection variable with the selected file name
            file_selection_var.set(file_name)

            # Update the folder path variable with the directory of the selected file
            folder_path_var.set(folder_path)

            # Clear the search box and reset the placeholder text
            search_var.set('Type to search...')
            search_entry.config(fg='grey')

            # Display the tags of the selected file
            display_selected_file_tags()

            # Update the file selection menu with DICOM files in the folder
            menu = file_selection_dropdown['menu']

            # Clear the existing menu items
            menu.delete(0, 'end')

            for file in dicom_files:
                # Add each DICOM file in the directory to the dropdown menu
                menu.add_command(label=file, command=lambda f=file: update_selected_file(f))

            # Set focus to the main window to ensure the search box loses focus
            root.focus()

        else: # If no DICOM files are found in the directory
            for i in tree.get_children():
                # Clear the existing tree view
                tree.delete(i)

            # Insert a message indicating no DICOM files were found
            tree.insert("", "end", values=("No DICOM files found in the selected folder.",))

def update_selected_file(file_name):
    """
    Update the selected file and display its tags.

    Inputs:
    file_name (str): The name of the selected DICOM file.

    Outputs: None
    """
    # Set the selected file name in the file selection variable
    file_selection_var.set(file_name)

    # Display the tags of the selected file
    display_selected_file_tags()

    # Check if the search box is not empty and does not contain the default placeholder
    if search_var.get().lower().strip() != "" and search_var.get() != "Type to search...":
        search_tags(None)  # Apply the current search text only if there is text in the search box


def display_selected_file_tags():
    """
    Display the tags of the selected DICOM file in the Treeview.

    Inputs: None
    Outputs: None
    """
    # Get the selected file name from the file selection variable
    file_name = file_selection_var.get()

    # Get the folder path from the folder path variable
    folder_path = folder_path_var.get()

    # Construct the full file path
    file_path = os.path.join(folder_path, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        # Print an error message if the file does not exist
        print(f"File does not exist: {file_path}")
        return

    # Parse the DICOM file to extract tag information
    dicom_data = parse_dicom(file_path)

    # Declare the original_data variable as global
    global original_data

    # Copy the parsed DICOM data to original_data
    original_data = dicom_data.copy()

    # Clear the existing tree view
    for i in tree.get_children():
        tree.delete(i)

    # Insert the parsed DICOM tags into the tree view
    for i, (tag_str, tag_name, vr, value) in enumerate(dicom_data):
        # Check if the Value Representation (VR) is 'OB' or 'OW'
        if vr in ['OB', 'OW']:
            # Display a placeholder for large binary values
            display_value = f"Not Loaded ({len(value)} bytes)"
        else:
            # Use the actual value for other VR types
            display_value = value

        # Insert the tag information into the tree view
        tree.insert("", "end", values=(tag_str, tag_name, vr, display_value),
                    tags=("evenrow" if i % 2 == 0 else "oddrow"))

    # Adjust the column widths based on the original data
    adjust_column_widths(original_data)

def adjust_column_widths(data):
    """
    Adjust the widths of the Treeview columns based on the content.

    Inputs:
    data (list): The DICOM data to be displayed.

    Outputs: None
    """
    # Get the font used by the Treeview from the style configuration
    style = ttk.Style()
    treeview_font = tkFont.nametofont(style.lookup("TLabel", "font"))

    # Iterate over each column in the Treeview
    for col in columns:
        # Determine the maximum length of the items in the current column
        max_item = max((str(row[idx]) for row in data for idx, name in enumerate(columns) if name == col), key=len,
                       default="")

        # Calculate the width based on the actual text of the item corresponding to max_length
        # Ensure the column header text is also considered in the maximum length
        width = treeview_font.measure(max_item) if len(max_item) > len(col) else treeview_font.measure(col)

        # Add padding to the width. Correcting for some unknown accuracy issue when measuring the font
        width += 10

        # Set the width of the column, and prevent it from stretching
        tree.column(col, width=width, stretch=tk.NO)

    # Allow the "Value" column to stretch
    tree.column("Value", stretch=tk.YES)

def search_tags(event):
    """
    Filter the displayed tags based on the search query.

    Inputs:
    event: The event that triggered the search.

    Outputs: None
    """
    # Get the search query
    query = search_var.get()

    # Clear all the existing rows in the Treeview
    tree.delete(*tree.get_children())

    # Check if the search query is empty or the default placeholder
    if query.lower().strip() == "" or query == "Type to search...":
        # If the search query is empty, use the original data
        display_data = original_data
    else:
        # Otherwise, filter the original data to include only items that match the search query
        display_data = [item for item in original_data if any(query in str(value).lower() for value in item)]

    # Insert the filtered tags into the tree view
    for i, (tag_str, tag_name, vr, value) in enumerate(display_data):
        # Check if the Value Representation (VR) is 'OB' or 'OW'
        if vr in ['OB', 'OW']:
            # Display a placeholder for large binary values
            display_value = f"Not Loaded ({len(value)} bytes)"
        else:
            # Use the actual value for other VR types
            display_value = value
        # Insert the tag information into the Treeview
        tree.insert("", "end", values=(tag_str, tag_name, vr, display_value),
                    tags=("evenrow" if i % 2 == 0 else "oddrow"))

def on_entry_click(event):
    """
    Clear the search entry when it is clicked.

    Inputs:
    event: The event that triggered the function.

    Outputs: None
    """
    # Check if the current text in the search entry is the placeholder
    if search_var.get() == 'Type to search...':
        # Clear the placeholder text
        search_var.set('')
        # Set the text color to black for user input
        search_entry.config(fg='black')

def on_focusout(event):
    """
    Restore the placeholder text in the search entry when it loses focus.

    Inputs:
    event: The event that triggered the function.

    Outputs: None
    """
    # Check if the search entry is empty
    if search_var.get() == '':
        # Restore the placeholder text
        search_var.set('Type to search...')
        # Set the text color to grey to indicate placeholder text
        search_entry.config(fg='grey')

if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    root.title("DICOM Tag Viewer")  # Set the window title

    frame = tk.Frame(root)  # Create a frame to hold the buttons and dropdown
    frame.pack(padx=10, pady=10)  # Add padding around the frame

    file_selection_var = tk.StringVar()  # Variable to store the selected file name
    folder_path_var = tk.StringVar()  # Variable to store the folder path
    search_var = tk.StringVar(value='Type to search...')  # Variable for the search entry with a placeholder text

    select_file_button = tk.Button(frame, text="Select DICOM File", command=select_file_and_display_data)  # Button to select a DICOM file
    select_file_button.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the button with padding

    file_selection_dropdown = tk.OptionMenu(frame, file_selection_var, "")  # Dropdown menu to select from available DICOM files
    file_selection_dropdown.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the dropdown with padding

    search_entry = tk.Entry(frame, textvariable=search_var, fg='grey')  # Entry widget for searching tags
    search_entry.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the entry with padding
    search_entry.bind('<FocusIn>', on_entry_click)  # Bind focus-in event to clear placeholder text
    search_entry.bind('<FocusOut>', on_focusout)  # Bind focus-out event to restore placeholder text
    search_entry.bind("<KeyRelease>", search_tags)  # Bind key release event to filter tags based on the search query

    tree_frame = tk.Frame(root)  # Frame to hold the Treeview and scrollbar
    tree_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Pack the frame with padding and allow it to expand

    columns = ("Tag", "Name", "VR", "Value")  # Define the columns for the Treeview
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")  # Create the Treeview widget with defined columns
    tree.heading("Tag", text="Tag")  # Set the heading for the "Tag" column
    tree.heading("Name", text="Name")  # Set the heading for the "Name" column
    tree.heading("VR", text="VR")  # Set the heading for the "VR" column
    tree.heading("Value", text="Value")  # Set the heading for the "Value" column

    tree.grid(row=0, column=0, sticky='nsew')  # Place the Treeview in the grid

    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)  # Create a vertical scrollbar for the Treeview
    tree.configure(yscroll=scrollbar.set)  # Configure the Treeview to use the scrollbar
    scrollbar.grid(row=0, column=1, sticky='ns')  # Place the scrollbar in the grid

    tree_frame.grid_rowconfigure(0, weight=1)  # Allow the first row of the grid to expand
    tree_frame.grid_columnconfigure(0, weight=1)  # Allow the first column of the grid to expand

    tree.tag_configure("evenrow", background="lightgrey")  # Configure the background color for even rows
    tree.tag_configure("oddrow", background="white")  # Configure the background color for odd rows

    # Set default window size
    root.geometry("800x600")  # Set the default size of the main window

    root.mainloop()  # Start the Tkinter main loop
