# -*-coding:utf-8-*-

from setuptools import setup

setup(
    name='RocketChatAPIBot',
    version='0.1.3',
    packages=['.', ],
    url='https://github.com/jadolg/RocketChatBot',
    license='MIT',
    author='Jorge Alberto Díaz Orozco',
    author_email='diazorozcoj@gmail.com',
    description='REST API based bot for Rocket.Chat',
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=(
        'rocketchat_API',
    )
)
