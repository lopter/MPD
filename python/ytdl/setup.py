import setuptools

version = "0.0.1.dev0"

setuptools.setup(
    name="mpd-ytdl",
    version=version,
    description="YoutubeDL integration glue for internal use by MPD",
    author="Louis Opter",
    author_email="louis@opter.org",
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points={"console_scripts": ["_mpd-ytdl = mpdy.main:main"]},
    install_requires=["youtube_dl"],
    tests_require=[
        "pytest>=3.0",
    ],
    extras_require={
        "dev": [
            "flake8",
            "ipython",
            "mypy",
            "pdbpp",
        ],
    },
    classifiers=[
        'Topic :: Multimedia :: Audio',
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        # 'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
