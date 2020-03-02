import logging
from importlib import import_module


class ObjectFactory:
    makers = {}

    def create(self, kind, lib_name, name, *args, **kwargs):
        key = f'{kind}.{lib_name}'
        extra_lib = f'extra_lib.{key}'
        if key not in self.makers:
            try:
                module = import_module(extra_lib)
                logging.info(f'loaded lib: {extra_lib}')
            except ModuleNotFoundError:
                try:
                    module = import_module(key)
                    logging.info(f'loaded lib: {key}')
                except ModuleNotFoundError:
                    null_key = f'{kind}.null'
                    module = import_module(null_key)
                    logging.info(f'loaded lib: {null_key}')
            self.makers[key] = module
        return getattr(self.makers[key], name)(*args, **kwargs)
