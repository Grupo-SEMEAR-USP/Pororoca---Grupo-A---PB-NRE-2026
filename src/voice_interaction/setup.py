from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'voice_interaction'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'voice_model'), glob(os.path.join('voice_model', 'wendel.onnx'))),
        (os.path.join('share', package_name, 'voice_model'), glob(os.path.join('voice_model', 'wendel.onnx.json'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='murilo',
    maintainer_email='muriloopires@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "voice_synthesizer = voice_interaction.voice_synthesizer:main",
            "text_emmiter = voice_interaction.text_emmiter:main"
        ],
    },
)
