from setuptools import find_packages, setup

package_name = "plant_vision"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="leo-vianna891",
    maintainer_email="226686012+leo-vianna891@users.noreply.github.com",
    description=(
        "Computer-vision tools for plant classification and visual tag detection."
    ),
    license="TODO: License declaration",
    entry_points={
        "console_scripts": [
            "train_classifier = plant_vision.cli.train:main",
            "evaluate_classifier = plant_vision.cli.evaluate:main",
            "predict_plant = plant_vision.cli.predict_image:main",
            "classify_camera = plant_vision.cli.classify_camera:main",
            "detect_tag_camera = plant_vision.cli.detect_tag_camera:main",
        ],
    },
)
