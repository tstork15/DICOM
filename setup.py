from setuptools import setup, find_packages

setup(
    name="dicom_tag_viewer",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pydicom",
    ],
    entry_points={
        "console_scripts": [
            "dicom_tag_viewer=dicomTagViewer:main",
        ],
    },
    author="Taggart Stork",
    description="A utility for viewing DICOM file tags using a graphical interface.",
    url="https://github.com/tstork15/dicom-tag-viewer",
)
