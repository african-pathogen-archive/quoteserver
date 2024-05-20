#!/usr/bin/env python

import html
import json
import os.path
import re

quotes_file = open(os.path.dirname(__file__) + '/../data/index.htm', encoding='windows-1252')

quotes: list[dict[str, str]] = []
source_re = re.compile(r'(?P<author>[^,]+), .*<a .*href=[^>]+>(?P<title>.*)</a> \((?P<year>\d{4})\)')
quote_num = 1
for line in quotes_file:
    if "<p>&#160;</p>" in line:
        quote = re.sub(r'<[^<]+>', '', next(quotes_file)).strip()
        source_line = next(quotes_file)
        source_match = source_re.match(source_line)
        if source_match is not None:
            source = source_match.groupdict()
            if source['author'] == 'Marx':
                source['author'] = 'Karl Marx'
            elif source['author'] == 'Engels' or source['author'] == '[Engels':
                source['author'] = 'Friedrich Engels'
            elif source['author'] == 'Marx and Engels' or source['author'] == 'Marx &amp; Engels':
                source['author'] = 'Karl Marx and Friedrich Engels'
            source['title']=  re.sub(r'<[^<]+>', '', html.unescape(source['title']))
            quotes.append({'quote': quote, 'id': str(quote_num), **source})
            quote_num += 1
print(json.dumps(quotes, indent=4, ensure_ascii=False))