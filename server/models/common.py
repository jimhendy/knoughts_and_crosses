from pydantic import BaseModel, Extra


class Model(BaseModel, extra=Extra.forbid):
    ...
