heroku create
heroku buildpacks:set https://github.com/kennethreitz/conda-buildpack
git push heroku master
