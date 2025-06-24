from setuptools import setup, find_packages

setup(
    name="taratool",
    version="0.1.0",
    description="Threat Analysis and Risk Assessment Tool",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here, e.g.:
        # 'Markdown',
    ],
    entry_points={
        'console_scripts': [
            'taratool=tara:main',
        ],
    },
    python_requires='>=3.8',
    include_package_data=True,
)
