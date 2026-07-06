import reapy_boost as rpr


def get_filenames():
    pr = rpr.Project()
    filenames = set()
    for item in pr.selected_items:
        filename = item.active_take.source.filename
        filenames.add(filename)
    return filenames


if __name__ == "__main__":
    print(get_filenames())
