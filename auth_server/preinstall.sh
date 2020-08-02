#!/bin/bash

echo 'Begin to install requirements.You should sudo. If failed, try again.'
echo 'If missing, use apt-get to install python3-lxml, which will be used in bs4'

pip3 install tornado jieba numpy scipy sklearn bs4 matplotlib wordcloud lda glove-python tensorflow keras
mkdir static
mkdir static/img
mkdir fingerprint/newArticleCache

echo 'Preparation success.'
