from functools import partial
from glob import glob
import pandas as pd
from tkinter import filedialog


def main():
    root = filedialog.askdirectory(title="Select root directory of annotations")
    output = filedialog.asksaveasfilename(title="Save as", filetypes=[("Excel file", ".xlsx")])

    annotation_filepaths = glob(f"{root}/**/*.stxsm", recursive=True)
    dataframes = map(partial(pd.read_xml, parser="etree"), annotation_filepaths)
    pd.concat(dataframes).to_excel(output, index=False)



if __name__ == "__main__":
    main()
