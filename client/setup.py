from setuptools import setup

setup(
    name="linechat",
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'linechat=linechat.cli:cli'
        ]
    }
)