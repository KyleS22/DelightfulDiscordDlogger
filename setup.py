from setuptools import setup

setup(
        name="delightful_discord_dlogger",
        version="0.1.0",
        packages=["delightful_discord_dlogger"],
        entry_points={
                'console_scripts': ['dddlog=delightful_discord_dlogger.cli:main'],
                },
        description="Simple logging with Discord webhooks",
        install_requires=['fire', 'requests'],
        setup_requires=['fire', 'requests']
        )
