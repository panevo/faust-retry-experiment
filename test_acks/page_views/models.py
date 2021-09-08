import faust


class PageView(faust.Record):
    id: str
    user: str
    retry: int =0
