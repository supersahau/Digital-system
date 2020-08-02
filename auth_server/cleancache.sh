#!/bin/bash

echo 'Start to clean cache...'
rm -rf __pycache__
rm -rf fingerprint/__pycache__
rm -rf visualization/__pycache__
rm -rf static/img/*
rm -rf fingerprint/newArticleCache/*
echo 'Completed'
