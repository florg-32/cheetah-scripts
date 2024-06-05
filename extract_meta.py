from functools import partial
from glob import glob
import pandas as pd
from tkinter import filedialog, messagebox
from os import path


def main():
    root = filedialog.askdirectory(title="Select root directory of annotations")
    output_file = filedialog.asksaveasfilename(
        title="Save as",
        filetypes=[("Excel file", ".xlsx"), ("Comma-separated values", ".csv")],
        defaultextension=".xlsx",
    )

    _, extension = path.splitext(output_file)
    if extension not in [".xlsx", ".csv"]:
        messagebox.showerror("Invalid file extension")
        exit(1)

    annotation_filepaths = glob(f"{root}/**/*.stxsm", recursive=True)
    dataframes = map(partial(pd.read_xml, parser="etree"), annotation_filepaths)
    output_frame = pd.concat(dataframes)

    if extension == ".xlsx":
        output_frame.to_excel(output_file, index=False)
    elif extension == ".csv":
        output_frame.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
