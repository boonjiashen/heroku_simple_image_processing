# What

Simple image processing Heroku app. This app returns a flipped image of the
user's uploaded image.

# Why

Skeleton code for scipy and numpy. With these two libraries a whole host of
image processing features can be enabled on the server side.

# Pre-requisites

Heroku toolbelt

# How to run locally

```bash
pip install -r requirements.txt
export FLASK_ENV=development
flask run
```

# How to deploy

    >> . run_remotely.sh

# Notes

Useful repos: [Scipy
buildpack](https://github.com/thenovices/heroku-buildpack-scipy), [Conda
buildpack](https://github.com/kennethreitz/conda-buildpack),
[Example use of Conda
buildpack](https://github.com/arose13/HerokuCondaScipyFlaskApp), [File uploader](http://code.runnable.com/UiPcaBXaxGNYAAAL/how-to-upload-a-file-to-the-server-in-flask-for-python)

We need the pillow package in requirements to enable scipy's imread
functionality. Without it, scipy.misc doesn't have the imread method.
