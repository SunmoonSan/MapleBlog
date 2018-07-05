#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 18-5-12 上午8:47
# @site  : https://github.com/SunmoonSan
import datetime
from haystack import indexes
from blog.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
