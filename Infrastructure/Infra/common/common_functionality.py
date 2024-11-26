import inspect
import sys


class CommonFunctionality:

    @staticmethod
    def find_class_by_name(search_string):
        found_classes = []

        for module_name, module in sys.modules.items():
            if module is None:
                continue

            classes = inspect.getmembers(module, inspect.isclass)
            for name, class_obj in classes:
                if search_string.lower() in name.lower():
                    found_classes.append((module_name, class_obj))

        return found_classes
