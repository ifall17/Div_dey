"""For my commpehension
    Setup.py is used for packages like pip"""
from setuptools import setup, find_packages
from typing import List


HYPEN_E_DOT = '-e .'
def get_requirement(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as fil_obj:
        requirements = fil_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements





setup(
    name="Ml_Project",
    version="0.0.1",
    author="Ibra S Fall",
    author_email="ifall736@gmail.com",
    packages=find_packages(),
    install_requires=get_requirement('requirements.txt')
)