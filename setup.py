from setuptools import setup, find_packages

# Load requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

config = dict(name="CloudHarvestCoreDataModel",
              version="0.1.0",
              description="This is the Core Data Model for CloudHarvest.",
              author="Cloud Harvest, Fiona June Leathers",
              license="CC Attribution-NonCommercial-ShareAlike 4.0 International",
              url="https://github.com/Cloud-Harvest/CloudHarvestCoreDataModel",
              packages=find_packages(),
              install_requires=requirements)

setup(**config)
