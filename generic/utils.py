from django.urls import get_resolver


def show_urls(urllist, depth=0):
    for entry in urllist:
        print("  " * depth, entry.pattern)
        if hasattr(entry, "url_patterns"):
            show_urls(entry.url_patterns, depth + 1)


show_urls(get_resolver().url_patterns)
