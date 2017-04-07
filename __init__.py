import aiohttp
import logging

from bs4 import BeautifulSoup

from opsdroid.matchers import match_regex, match_crontab


_LOGGER = logging.getLogger(__name__)
_MAGPI_BASE_URL = "https://www.raspberrypi.org/magpi-issues"


async def get_issue_list():
    issues = []
    async with aiohttp.ClientSession() as session:
        async with session.get(_MAGPI_BASE_URL) as resp:
            soup = BeautifulSoup(await resp.text(), "html.parser")
            for link in soup.findAll('a'):
                if ".pdf" in link.get('href'):
                    issues.append("{}/{}".format(_MAGPI_BASE_URL, link.get('href')))
    return issues

@match_regex(r'.*magpi ([0-9]+).*')
async def get_issue(opsdroid, config, message):
    issue = message.regex.group(1).zfill(2)
    _LOGGER.debug("Looking for magpi issue %s pdf", issue)
    issues = await get_issue_list()
    matches = [x for x in issues if "MagPi{}.pdf".format(issue) in x]
    if len(matches) > 0:
        for link in matches:
            await message.respond(link)
    else:
        await message.respond("Cannot find issue {}".format(issue))

@match_crontab('0 * * * *')
async def announce_new_issue(opsdroid, config, message):
    if message is None:
        message = Message("",
                          None,
                          config.get("room", opsdroid.default_connector.default_room),
                          opsdroid.default_connector)
    known_issues = await opsdroid.memory.get("magpi-issues")
    current_issues = await get_issue_list()
    try:
        if known_issues is None:
            _LOGGER.debug("No magpi issues in memory, skipping...")
            return
        new_issues = [issue for issue in current_issues if issue not in known_issues]
        for issue in new_issues:
            _LOGGER.debug("Found a new magpi issue")
            await message.respond("There's a new issue of MagPi:\n{}".format(issue))
    finally:
        await opsdroid.memory.put("magpi-issues", current_issues)
