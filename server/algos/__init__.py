from . import feed, dummy
from server import config

uri = config.FEED_URI

algos = {uri: dummy.handler, "legacy": feed.handler}
