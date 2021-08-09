
from aiohttp import ClientSession
import asyncio
import pathlib


async def fetch(url, session, year):
    async with session.get(url) as response:
        html_body = await response.read()
        return {"body": html_body, "year": year}


async def fetch_with_sem(sem, session, url, year=None):
    async with sem:
        return await fetch(url, session, year)


async def main(start_year=2020, years_ago=5):
    html_body = ""
    tasks = []
    # semaphore
    sem = asyncio.Semaphore(10)

    async with ClientSession() as session:
        for i in range(0, years_ago):
            year = start_year - i
            url = f"https://www.boxofficemojo.com/year/{year}/"
            print("year", year, url)
            tasks.append(asyncio.create_task(
                fetch_with_sem(sem, session, url, year=None)
            )
            )

            pages_content = await asyncio.gather(*tasks)
            return pages_content


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


results = asyncio.run(main())

outputdir = pathlib.Path().resolve() / "snapshots"
outputdir.mkdir(parents=True, exist_ok=True)


for result in results:
    current_year = result.get("year")
    htmldata = result.get("body")
    output_file = outputdir / "2020.html"
    output_file.write_text(htmldata.decode(), encoding="utf-8")
