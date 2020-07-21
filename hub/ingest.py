import pandas as pd
import numpy as np

RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"

HUB_COLUMNS = {
    "PROJECT NAME": "project_name",
    "LINK": "link",
    "LOCAL FILE": "local_file",
    "PROJECT CATEGORY": "project_category",
    "INCLUDE IN DIGITAL HUB": "show",
    "DATA": "data",
    "KEYWORDS": "keywords",
    "CARD SIZE": "card_size",
    "ANNOUNCEMENT": "announcement",
    "ORDERING": "ordering",
    "STATUS": "status",
    "CARD IMAGE-HI": "card_image_hi",
    "CARD IMAGE-LO": "card_image_lo",
}


def string_to_array(series):
    def item_to_array(item):
        if item is np.NaN:
            item = []
        else:
            item = item.split(",")

        item = [x.strip() for x in item]
        item = str(item).replace("[", "{").replace("]", "}").replace("'", "")
        return item

    return series.apply(item_to_array)


def string_to_bool(series):
    def truthy(item):
        if str(item).lower() in ["yes", "true", "y", "t", "1", "1.0"]:
            return True
        else:
            return False

    return series.apply(truthy)


def format_enum(string):
    if string is np.NaN:
        return np.NaN
    else:
        return string.lower().replace(" / ", "_").replace(" ", "_")


if __name__ == "__main__":
    projects = pd.read_csv(
        f"./{RAW_DATA_DIR}/Growth Lab Digital Hub_Master List - Sheet1.csv"
    )

    projects.columns = [x.strip() for x in projects.columns]
    projects = projects.rename(columns=HUB_COLUMNS)

    projects.show = string_to_bool(projects.show)

    projects.keywords = string_to_array(projects.keywords)
    projects.data = string_to_array(projects.data)

    projects.announcement = projects.announcement.apply(
        lambda x: x if x != "None" else np.NaN
    )

    projects.project_category = projects.project_category.apply(format_enum)
    projects.card_size = projects.card_size.apply(format_enum)
    projects.status = projects.status.apply(format_enum)

    projects.to_csv(f"./{PROCESSED_DATA_DIR}/projects.csv", index=False)
