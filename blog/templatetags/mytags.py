#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 18-5-25 上午12:39
# @site  : https://github.com/SunmoonSan
from django import template

register = template.Library()


@register.simple_tag
def pagination(current_page,paginator, num_of_displaypages=10, num_of_backpages=4):
    #  current_page is a django.core.paginator.Page 's instance
    #  paginator is a django.core.paginator.Paginator 's instance
    #
    num_of_frontpages = num_of_displaypages - num_of_backpages - 3
    html = ''

    if paginator.num_pages <= num_of_displaypages :
        for i in range(1,paginator.num_pages+1):
            html+= '<li ><a href="?page=%s">%s </a></li>'%(i,i)
        return html

    elif current_page.number <= num_of_displaypages-num_of_backpages:
        for i in range(1,num_of_displaypages+1):
            html+= '<li ><a href="?page=%s">%s </a></li>'%(i,i)
        return html

    elif num_of_displaypages-num_of_frontpages <= current_page.number <= paginator.num_pages-num_of_backpages :
        html = '''
            <li><a href="?page=1">1</a></la>
            <li class="disabled"><a href="?page=1">...</a></la>
        '''
        for i in range(current_page.number-num_of_frontpages,current_page.number+num_of_backpages+1):
            html+='<li><a href="?page=%s">%s</a></la>'%(i,i)
        return html

    else:
        html = '''
            <li><a href="?page=1">1</a></la>
            <li class="disabled"><a href="?page=1">...</a></la>
        '''
        for i in range(paginator.num_pages-num_of_backpages-num_of_frontpages,paginator.num_pages+1):
            html+='<li><a href="?page=%s">%s</a></la>'%(i,i)
        return html
