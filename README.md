# Fake_news

This repository contains code to replicate the findings of the Vicario et al. paper, whose
main finding was the presence of echo chambers on social networks.

In this study, we gather data from Twitter as opposed to Facebook, as such the analysis
is slightly different.

## What this repo does

* Gathers the data
  - uses curl requests to query data from the PanaceaLab dataset
  - unzips the tweet ID txt files
  - subsamples these tweet IDs to reduce the dataset size
  - hydrates the tweet IDs to produce jsonl files of tweet json objects
  
* Generates hashtag polarities
  - hashtag polarities represent how much more often the hashtag appears in a marker subset in comparison to the baseline set
  
* Runs code to generate user polarities given two tweets
  - input is a tweet, one science and one misinformation
  - output is the user polarities for the users that retweeted the input tweet

* Generates plots of user polarity distributions as well as EDA plots

## Running the project
* To get the data from Twitter, create a developer account and get your developer keys
* Configure `twarc`
  - On the terminal, run `twarc configure`
  - Supply keys made earlier

### Building the preoject using `run.py`
* To get the data, from the project root dir, run `python run.py data`
  - This downloads the data from Twitter in the directory specified in
    `config/data_params.yaml`.
* To get basic plots of data, from the project root dir, run `python run.py eda`
  - This creates several plots about the data as well as the distribution of user polarities of specified tweet ids. These are stored in the directory specified in
    `config/eda_params.yaml`.
