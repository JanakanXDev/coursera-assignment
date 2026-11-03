import collections
import collections.abc

for attribute in (
    'Callable',
    'Mapping',
    'MutableMapping',
    'Sequence',
    'Iterable',
    'Set',
):
    if not hasattr(collections, attribute):
        setattr(collections, attribute, getattr(collections.abc, attribute))
