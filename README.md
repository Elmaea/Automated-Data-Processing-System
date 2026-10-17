# Archived Data Retrieval and Analysis Tool

## Overview
A Python-based desktop application developed as part of my industry internship project. It supports retrieving, decrypting, filtering, and analyzing archived time-series data through a graphical user interface (GUI).

## Features
- GUI for selecting data directories and files
- Decryption of supported encrypted archives
- Date-time and Unix epoch timestamp handling
- Data filtering by time range and sampling interval
- Parameter selection and CSV export
- Data visualization, basic analysis, and report generation

## Technology Stack
Python, Tkinter, Pandas, Matplotlib, Tkcalendar, Python-docx, and OpenSSL.

## Installation needed
pip install pandas matplotlib tkcalendar python-docx mplcursors

## General Workflow

The intended workflow is:

1.Launch the desktop application.\n
2.Select the directory containing the supported archived data.
3.Run the decryption operation.
4.Select the required data file, parameters, or identifiers.
5.Specify the required time range and sampling interval, where applicable.
6.Retrieve and filter the relevant data.
7.Inspect the resulting data and available visualizations.
8.Export supported outputs for further analysis or reporting.

## Compatibility
The application is designed for data files that follow the specific formats, structures, metadata conventions, and configurations expected by the project. It is intended to work with compatible files matching these requirements; files in other formats may require modifications to the code.

## Disclaimer
This project is shared for reference and demonstration purposes only. It is not intended to be a ready-to-run, general-purpose application. Its functionality depends on compatible input files, supporting scripts, external tools, dependencies, and system configuration.
