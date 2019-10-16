from distutils.core import setup

setup(
    name="gravitational-audition",
    version="0.1.0",
    author="Walt Della",
    author_email="walt@javins.net",
    description="A coding audition via a docker API test case.",
    url="https://github.com/javins/gravitational-audition",
    packages=['grav'],
    package_dir={'': 'src'},
    package_data={'grav': 'wellknown.tgz'},
    include_package_data=True,
)
