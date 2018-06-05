# what else should be defined here? seems useless
# to have just one use for common.py

import attr # rewrite without attr

@attr.s
class Item:
    title = attr.ib()
    text = attr.ib()
