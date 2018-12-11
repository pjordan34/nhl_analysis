from setuptools import setup,find_packages



with open("requirements.txt") as f:
	required = f.read().splitlines()

setup(
		name="nhl_analysis",
		author = "Patrick Jordan",
		description="package to conduct anlysis on NHL play by play data",
		license="MIT",
		packages=find_packages('src'),
		package_dir={'': 'src'},
		url="https://github.com/pjordan34/nhl_analysis.git",
		install_requires=list(required),
		version="0.0"
	)
