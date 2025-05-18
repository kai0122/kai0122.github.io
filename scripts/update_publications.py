#!/usr/bin/env python3
import json
from scholarly import scholarly

GSCHOLAR_ID = "0gl__ukAAAAJ"

def fetch_publications():
    author = scholarly.search_author_id(GSCHOLAR_ID)
    author = scholarly.fill(author, sections=['publications'])
    pubs = []
    for p in author['publications']:
        entry = scholarly.fill(p)
        # print(entry)
        pubs.append({
            'authors': entry.get('bib', {}).get('author', ''),
            'year': entry.get('bib', {}).get('pub_year', ''),
            'title': entry.get('bib', {}).get('title', ''),
            'journal': entry.get('bib', {}).get('citation', ''),
            'url': entry.get('pub_url', '#'),
            'citations': entry.get('num_citations', 0)
        })
    return pubs

if __name__ == "__main__":
    data = {'publications': fetch_publications()}
    with open('publications.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
