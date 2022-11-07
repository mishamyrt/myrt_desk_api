import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

long_description = 'asd'

setuptools.setup(
    name="myrt_desk_api",
    version="0.1.1",
    author="Mikhael Khrustik",
    description="Library for controlling smart bulbs that are controlled by the DoIT protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        'myrt_desk_api',
        'myrt_desk_api.backlight',
        'myrt_desk_api.legs',
        'myrt_desk_api.system',
        'myrt_desk_api.datagram',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.7',
    package_dir={'':'.'},
    scripts=['myrt_desk']
)
