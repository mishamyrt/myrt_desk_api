"""MyrtDesk setup script"""
import setuptools

with open(".version", "r", encoding="utf-8") as fh:
    version = fh.read()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="myrt_desk_api",
    version=version,
    author="Mikhael Khrustik",
    description="Library for controlling smart bulbs that are controlled by the DoIT protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'myrt_desk_api',
        'myrt_desk_api.backlight',
        'myrt_desk_api.legs',
        'myrt_desk_api.system',
        'myrt_desk_api.transport',
        'myrt_desk_api.cli',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
        'asyncio-datagram==1.4.0',
        'arrrgs==3.1.0',
        'typing-extensions==4.8.0',
        'async_timeout==4.0.3'
    ],
    python_requires='>=3.7',
    package_dir={'':'.'},
    scripts=['scripts/myrt_desk']
)
