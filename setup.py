from setuptools import setup, find_packages

setup(
    name="thesisproject",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.24.0,<2.0.0",
        "pandas>=2.2.3,<3.0.0",
        "matplotlib>=3.10.0,<4.0.0",
        "scikit-learn>=1.6.1,<2.0.0",
        "tqdm>=4.67.1,<5.0.0",
        "langchain>=0.3.23,<0.4.0",
        "langchain-openai>=0.3.12,<0.4.0",
        "langchain-google-genai>=2.1.2,<3.0.0",
    ],
) 