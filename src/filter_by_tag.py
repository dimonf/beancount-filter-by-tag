"""Filter transactions on tags

Select all transactions that:
  - do not have tags, specified by 'exclude', and
  - do have tags, specified by 'include'

plugin "beancount_filter_by_tag" "{'include':'budget,capital', 'exclude':'trading,commercial'}"

if no 'include' option is specified, than any transaction's tag is accepted, unless it is
rejected by 'exclude' option. If a transaction has tags that specified in both, 'include' and 
'exlude' options, than 'exclude' wins.
"""
__copyright__ = "Copyright (C) Dmitri Kourbatsky"
__license__ = "MIT License"
__plugins__ = ('filter_by_tag',)

from beancount.core  import data
from beancount.parser import options

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
        if not isinstance(entry, data.Transaction):
            return True
        elif not entry.tags:
            if not tags_in:
                return True
            else:
                return False
        else:
            entry_tags = set(entry.tags)
            if tags_ex and (tags_ex & entry_tags):
                return False
            elif tags_in: 
                if not tags_in & entry_tags:
                    return False
            else:
                return True

    filtered_entries = [entry for entry in entries if tag_check(entry)]
    return (filtered_entries, [])

