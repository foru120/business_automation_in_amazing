import dataclasses as dc

from unpackable import Unpackable


@dc.dataclass(unsafe_hash=True)
class Tag(Unpackable):
    code: str
    top_code: str
    name: str

    def to_list(self):
        return [self.code, self.top_code, self.name]