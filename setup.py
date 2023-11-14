from setuptools import setup

setup(
    name='pylibdatachannel',
    version='0.19.3',
    py_modules=['pylibdatachannel'],
    setup_requires=["cffi>=1.0.0"],
    install_requires=[
        ["cffi>=1.0.0"],
    ],
    cffi_modules="pylibdatachannel_build.py:ffibuilder"
)
