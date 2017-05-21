from setuptools import setup, find_packages

setup(
    name='my_oauth_playground',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.2',

    # The project's main homepage.
    url='https://github.com/gy-chen/my-oauth-playground',

    # Author details
    author='GYCHEN',
    author_email='gy.chen@gms.nutc.edu.tw',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['flask',
                      'oauth2client',
                      'google-api-python-client',
                      'PyJWT',
                      'six'],
)
