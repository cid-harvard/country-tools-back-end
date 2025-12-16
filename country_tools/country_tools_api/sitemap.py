import os
from flask import render_template_string, make_response
import pandas as pd

from country_tools.country_tools_api.database.base import db_session
from country_tools.country_tools_api.database.hub import HubProjects


SITEMAP_TEMPLATE = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    "{% for url in urls %}"
    "    <url>"
    "        <loc>{{ url }}</loc>"
    "        <lastmod>{{ update_date }}</lastmod>"
    "        <changefreq>yearly</changefreq>"
    "    </url>"
    "{% endfor %}"
    "</urlset>"
)


def generate_sitemap(update_date):
    base_url = "https://growthlab.app"

    static_pages = [
        "",
        "community",
        "about",
    ]

    urls = [os.path.join(base_url, page) for page in static_pages]

    projects = [
        x[0]
        for x in db_session.query(HubProjects.link)
        .filter(HubProjects.show.is_(True))
        .filter(HubProjects.link.contains("growthlab.app"))
        .all()
    ]

    urls.extend(projects)

    template = render_template_string(
        SITEMAP_TEMPLATE,
        urls=urls,
        update_date=update_date,
    )

    response = make_response(template)
    response.headers["Content-Type"] = "application/xml"

    return response
