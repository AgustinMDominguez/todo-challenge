import ast

from project.logger import Logger
from todo.request_utils import (
    get_datetime
)


log = Logger.logger()


class FilterDictValidator():
    def __init__(self, dictionary) -> None:
        self.initdic = dictionary
        self.args_schema = {
            "parent_id": int,
            "title": str,
            "description": str,
            "favorite": bool,
            "page": int,
            "search_sub_tree": bool,
            "done": bool,
        }

    def validate_updateable_fields(self):
        include = [
            "done",
            "tags",
            "title",
            "favorite"
            "parent_id",
            "description"
        ]
        return self._get_validated_dictionary(include)

    def validate_search_dictionary(self):
        include = [
            "page",
            "done",
            "tags",
            "title",
            "end_time",
            "favorite",
            "parent_id",
            "start_time",
            "search_sub_tree",
        ]
        return self._get_validated_dictionary(include)

    def _get_validated_dictionary(self, include: list = []):
        log.debug(f"_get_validated_dictionary include: {include}")
        valid_dic = {}
        args_schema = self.args_schema.copy()
        exclude_args = []
        for arg in args_schema.keys():
            if arg not in include:
                exclude_args.append(arg)
        for exclude_arg in exclude_args:
            args_schema.pop(exclude_arg)

        tags = self.initdic.get("tags", None)
        if tags is not None and "tags" not in include:
            try:
                assert isinstance(tags, list)
                for tag in tags:
                    assert isinstance(tag, str)
                valid_dic["tags"] = tags
            except Exception as e:
                log.error(f"Tags '{tags}' are malformed. Error: {e}")

        for arg in args_schema:
            if arg in self.initdic.keys():
                try:
                    if isinstance(self.initdic[arg], args_schema[arg]):
                        valid_dic[arg] = self.initdic[arg]
                    else:
                        eval = ast.literal_eval(self.initdic[arg])
                        if isinstance(eval, args_schema[arg]):
                            valid_dic[arg] = eval
                        else:
                            raise ValueError()
                except Exception as e:
                    log.error(e)
                    log.error(
                        f"argument {arg} is not {args_schema[arg]}. Arg:"
                        f" {self.initdic[arg]} of type {type(self.initdic[arg])}"
                    )

        start_time = get_datetime(self.initdic.get("start_time", None))
        if start_time is not None and "start_time" not in include:
            valid_dic["start_time"] = start_time
        end_time = get_datetime(self.initdic.get("end_time", None))
        if end_time is not None and "end_time" not in include:
            valid_dic["end_time"] = end_time

        return valid_dic