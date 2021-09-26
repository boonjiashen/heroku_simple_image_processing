# What

~~Simple image processing app deployed to <https://mosaic.boonjiashen.com/>.~~

Since I've rearchitected this webapp to be serverless and off of Heroku, I've moved the repo to https://github.com/boonjiashen/photomosaic-infra and I'm no longer maintaining this repo.

This repo remains here as an archive.

# How to run locally

```bash
pip install -r requirements.txt
export FLASK_ENV=development && flask run
```

# Run unit tests

```bash
python -m unittest
```
