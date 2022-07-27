"""This plugin acts as filter on the ground of tag(s). Only transactions that
satisfy criteria are included in bean query result. Plugin shall be activated
in beancount source file like this:

plugin "beancount_filter_by_tag" "{'include':'budget', 'exclude':'trading'}"

where 'include' specifies tags which must be present, while 'exclude' acts oposite.
Both, 'include' and 'exclude' are optional; only one of them must be specified.
All criteria are combined on AND logic. 'exclude' directive prevails over 'include'.
A single tag or tags, separated by comma, can be specified, eg {'include':'tag_a,tag_b'}.
Space-only (' ') and empty ('') tags, specified as arguments, are ignored.
"""
__copyright__ = "Copyright (C) Dmitri Kourbatsky"
__license__ = "MIT License"



from beancount.core  import data
from beancount.parser import options

__plugins__ = ('filter_by_tag',)

def filter_by_tag(entries, options_map, config_str):
    tags = eval(config_str, {}, {})
    if not isinstance(tags, dict):
        raise RuntimeError("Invalid plugin configuration: args must be a single dictionary")
    #convert tag(s) into a set, removing spaces and space-only tags (if any)
    tags_in = tags.get('include')
    tags_in = set([t.strip() for t in tags_in.split(',') if t.strip()]) if tags_in else set()
    tags_ex = tags.get('exclude')
    tags_ex = set([t.strip() for t in tags_ex.split(',') if t.strip()]) if tags_ex else set()
    #
    def tag_check(entry):
        if not entry.tags:
            if not tags_in:
                return True
            else:
                return False
        else:
            entry_tags = set(entry.tags)
            if tags_ex & entry_tags:
                return False
            elif tags_in & entry_tags:
                return True
            else:
                return False

    filtered_entries = [entry for entry in entries if tag_check(entry)]
    return (filtered_entries, [])

