import pandas as pd
import numpy as np

RAW_DATA_DIR = "./raw_data"
PROCESSED_DATA_DIR = "./processed_data"


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
        if item.lower() in ["yes", "true", "y", "t"]:
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
        f"./{RAW_DATA_DIR}/Growth Lab Digital Hub_Master List - HUB.csv"
    )

    projects.columns = [x.lower().strip().replace(" ", "_") for x in projects.columns]
    projects = projects.rename(columns={"include_in_digital_hub": "show"})

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
