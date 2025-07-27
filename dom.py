class Element:
    name: str
    attributes: dict
    children: list
    content: str
    parent: any

    def __init__(self, name):
        self.name = name
        self.attributes = {}
        self.children = []
        self.content = ""

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def html(self) -> str:
        # open start tag
        res = f"<{self.name}"

        # attributes
        for key, value in self.attributes.items():
            res += f' {key}="{value}"'

        # close start tag
        res += ">\n"

        # add "raw" content
        if self.content:
            res += self.content + "\n"

        # add children
        for child in self.children:
            res += child.html() + "\n"

        # end tag
        res += f"</{self.name}>"

        return res

def notification(title):
    notif = Element("div")
    notif.attributes["id"] = "notification"

    title_elem = Element("p")
    title_elem.content = title
    notif.add_child(title_elem)

    return notif

def refresh(time: int, url: str):
    meta = Element("meta")
    meta.attributes["http-equiv"] = "refresh"
    meta.attributes["content"] = f"{time}; URL={url}"

    return meta