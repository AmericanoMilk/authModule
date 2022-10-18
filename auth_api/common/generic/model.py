from itertools import chain



def get_model_dict(model, fields=None, exclude=None):
    opts = model._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(model)
    return data


def get_queryset_list_dict(queryset_list, fields=None, exclude=None):
    data = [get_model_dict(i, fields=fields, exclude=exclude) for i in queryset_list]
    return data
