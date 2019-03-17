from setuptools import setup, find_packages


def load_requirements(filename: str):
    """ load requirements from a pip requirements file """
    line_iter = (line.strip() for line in open(filename))
    return [line for line in line_iter if line and not line.startswith("#")]


setup(
    name='url-shortener',
    version='0.0.1',
    author='CAMCOH1989',
    author_email='camcoh1989@gmail.com',
    license='MIT',
    description='URL shortening service',
    long_description=open('README.rst').read(),
    platforms="all",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': [
            'url-shortener-api = url_shortener.main:main'
        ]
    },
    packages=find_packages(exclude=['tests']),
    install_requires=load_requirements('requirements.txt'),
    python_requires=">3.4.*, <4",
    extras_require={
        'develop': load_requirements('requirements.dev.txt'),
    },
    url='https://github.com/CAMCOH1989/url-shortener'
)
