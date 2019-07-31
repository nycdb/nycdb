from nycdb.dataset_transformations import to_csv


def myplugin_custom_dataset(dataset):
    return to_csv(dataset.files[0].dest)
