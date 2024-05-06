import yaml

from ExcelLoader import ExcelLoader
from Visualization import Visualization


if __name__ == "__main__":

    # read yaml file
    with open("./config.yml", 'r') as file:
        config = yaml.safe_load(file)

    # read excel file
    excel_loader = ExcelLoader()
    excel_loader.load(config["init"]["excel_dir"])

    # create contents
    visualizer = Visualization(excel_loader, config)
    visualizer.visualize()
