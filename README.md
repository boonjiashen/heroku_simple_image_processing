#What

Simple image processing Heroku app. This app returns a flipped image of the
user's uploaded image.

#Why

Skeleton code for scipy and numpy. With these two libraries a whole host of
image processing features can be enabled on the server side.

#Pre-requisites

Heroku toolbelt

#How to run

    >> . run_remotely.sh

#Notes

Useful repos: [Conda
buildpack](https://github.com/kennethreitz/conda-buildpack),
[Example use of Conda
buildpack](https://github.com/arose13/HerokuCondaScipyFlaskApp)

We need the pillow package in conda requirements to enable scipy's imread
functionality. Without it, scipy.ndimage.imread throws an import error (haven't
tested with scipy.misc.imread, which we're using in this example).

Moved all requirements from pip to conda, to simplify local build:

    >> conda create --name <env-name> --file conda-requirements.txt
    >> . activate <env-name>

Removed version names in conda requirement file because specifying them seemed
to cause a conflict between the Fortran library and scipy. With version names
scipy would throw an error about not finding the Fortran shared library. This
seemed to be resolved by removing version names and allowing conda to manage
versions.
