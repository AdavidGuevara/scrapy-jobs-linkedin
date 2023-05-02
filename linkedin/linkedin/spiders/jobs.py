import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Ciencia+de+datos&location=Colombia&geoId=100876405&trk=public_jobs_jobs-search-bar_search-submit&start={}"
    custom_settings = {
        "FEED_URI": "jobs.json",
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def start_requests(self):
        first_page = 0
        first_url = self.base_url.format(first_page)
        yield scrapy.Request(
            url=first_url, callback=self.parse, meta={"first_page": first_page}
        )

    def parse(self, response):
        first_page = response.meta["first_page"]

        jobs = response.css("li")
        for job in jobs:
            yield {
                "title": job.css("h3::text").get(default="not-found").strip(),
                "url": job.css(".base-card__full-link::attr(href)").get(default="not-found"),
                "date_post": job.css("time::text").get(default="not-found").strip(),
                "company": job.css("h4 a::text").get(default="not-found").strip(),
            }

        if len(jobs) > 0:
            first_page = int(first_page) + 25
            next_url = self.base_url.format(first_page)
            yield scrapy.Request(
                url=next_url, callback=self.parse, meta={"first_page": first_page}
            )
