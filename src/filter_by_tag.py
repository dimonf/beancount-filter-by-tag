"""Filter transactions on tags

Select all transactions that:
  - do not have tags, specified by 'exclude', and
  - do have tags, specified by 'include'

plugin "beancount_filter_by_tag" "{'include':'budget,capital', \
                                   'exclude':'trading,commercial' \
                                   'opts':'no-bal,something else'}"

if no 'include' option is specified, than any transaction's tag is accepted, unless it is
rejected by 'exclude' option. If a transaction has tags that specified in both, 'include' and 
'exlude' options, than 'exclude' wins.
other options can be specified:
  - no-bal: block 'balance' entries in journal, as filtering on transactions most likely will make 
    this function raising error
"""
__copyright__ = "Copyright (C) Dmitri Kourbatsky"
__license__ = "MIT License"
__plugins__ = ('filter_by_tag',)

from beancount.core  import data
from beancount.parser import options

_DEBUG = False

def filter_by_tag(entries, options_map, config_str):
    tags = eval(config_str, {}, {})
    if not isinstance(tags, dict):
        raise RuntimeError("Invalid plugin configuration: args must be a single dictionary")
    #convert tag(s) into a set, removing spaces and space-only tags (if any)
    tags_in = tags.get('include')
    tags_in = set([t.strip() for t in tags_in.split(',') if t.strip()]) if tags_in else set()
    tags_ex = tags.get('exclude')
    tags_ex = set([t.strip() for t in tags_ex.split(',') if t.strip()]) if tags_ex else set()
    ignore_bal_check = False
    other_opts = tags.get('opts', False)
    if other_opts:
        ignore_bal_check = 'no-bal' in other_opts
    #
    flag_bal_ignored = False

    def tag_check(entry):
        nonlocal flag_bal_ignored

        if ignore_bal_check and isinstance(entry, data.Balance):
            flag_bal_ignored = True
            return False
        elif not isinstance(entry, data.Transaction):
            return True

        if _DEBUG:
            print({'tags_in':tags_in,'tags_ex':tags_ex,'entry.tags':entry.tags} )

        if not entry.tags:
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
            else:
                return True

    filtered_entries = [entry for entry in entries if tag_check(entry)]
    if flag_bal_ignored:
        print('  !!! balance assertion directives in data file(s) are ignored !!!')
    return (filtered_entries, [])

