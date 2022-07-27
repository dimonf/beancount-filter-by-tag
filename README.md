# beancount-filter-by-tag


beancount plugin which filter transactions on tags.

There is an "exclude_tag" plugin, shipped with beancount, which allows to exclude transactions,
ignores transactions tagged as 'virtual'. This plugin is more versatile, as it can be configured
to include transactions with certain tag ('include' argument), as well as exclude transactions 
('exclude' argument). Exclude always wins and multiple criteria are combined by logical AND.

include this directive in source file:

plugin "beancount_filter_by_tag.filter_by_tag" "{'include':'budget,travel', 'exclude':'trading'}"

This plugin may help, for example, if accounting records are stored in number of files and it is
desirable to limit scope of work. Say, master file ('M') contains all bank transactions, while a 
separate file ('P') comprises transactions related to a specific project. In file P:

include "/master.bean"

plugin "beancount_filter_by_tag.filter_by_tag" "{'include':'project-P'}"
pushtag #project-P

Then, in file M, transactions, related to the project, can be tagged with #project-P. Having this,
fava or bean-query can be run on M file, limiting the user's work to the project's data.
