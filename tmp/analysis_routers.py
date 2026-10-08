import sys

sys.path.insert(0, '/home/sasha/work/bots/banyaSveta')

from bot.routers import router  # noqa: E402


def walk(r):
    yield r
    for sub in r.sub_routers:
        yield from walk(sub)


for r in walk(router):
    for observer in r.message.handlers:
        print('message :', observer.callback.__name__)
    for observer in r.callback_query.handlers:
        print('callback:', observer.callback.__name__)
