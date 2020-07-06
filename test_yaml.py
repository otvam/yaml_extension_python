import load_yaml


if __name__ == "__main__":
    """
    Test code for the load_yaml function.
    """

    # load a yaml file
    data = load_yaml.load_yaml('test_data/test_main.yaml')

    # display the data
    print(data)