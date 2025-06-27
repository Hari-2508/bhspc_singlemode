from setuptools import setup, find_packages

setup(
    name='bhspc_singlemode',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    author='Harish Purushothaman',
    author_email='harishpurushothaman23@gmail.com',
    description='Python wrapper for Becker & Hickl SPC modules single mode measurements',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows'
    ],
    python_requires='>=3.8'
)
