# -*-coding:utf-8-*-

from setuptools import setup

setup(
    name='RocketChatBot',
    version='0.1',
    packages=['RocketChatBot', ],
    url='https://github.com/jadolg/RocketChatBot',
    license='MIT',
    author='Jorge Alberto Díaz Orozco',
    author_email='diazorozcoj@gmail.com',
    description='REST API based bot for Rocket.Chat',
    long_description=open("README.md", "r").read(),
    install_requires=(
        'rocketchat_API',
    )
)
