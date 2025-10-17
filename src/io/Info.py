from typing import Dict, Any, List

class Info:
    def __init__(self):
        """Initialize storage for infos and sections."""
        self.infos: Dict[str, Any] = {}
        self.sections: List[tuple] = []

    def addInfo(self, key: str, value: Any) -> None:
        """Add a key-value information entry."""
        self.infos[key] = value

    def addSection(self, title: str, content: str) -> None:
        """Add a titled section with multiline content."""
        self.sections.append((title, content))

    def display(self) -> None:
        """Print the rendered output to console."""
        print(self.render())

    def render(self) -> str:
        """Build and return the formatted ASCII report string."""
        if not self.infos and not self.sections:
            return ""

        def border(w: int, ch: str) -> str:
            """Return a border line of given width using character."""
            return "+" + ch * w + "+\n"

        def center_line(text: str, w: int) -> str:
            """Return a centered text line within borders."""
            return "|" + text.center(w) + "|\n"

        result = ""

        if self.infos:
            maxKey = max((len(str(k)) for k in self.infos), default=0)
            maxVal = max((len(str(v)) for v in self.infos), default=0)

            inner_w = max(maxKey + 3 + maxVal + 2, 40)
            inner_w = min(inner_w, 80)

            result += border(inner_w, "=")
            result += center_line(" INFORMASI OPTIMASI ", inner_w)
            result += border(inner_w, "=") + "\n"

            result += border(inner_w, "-")
            result += center_line(" PARAMETER & HASIL ", inner_w)
            result += border(inner_w, "-")

            for k, v in self.infos.items():
                k_s = str(k).ljust(maxKey)
                v_s = str(v).rjust(maxVal)
                line = f"| {k_s} : {v_s} |"
                result += line + "\n"

            result += border(inner_w, "-") + "\n"

        for title, content in self.sections:
            lines = content.split("\n") if content else [""]
            max_line = max((len(l) for l in lines), default=0)

            inner_w = max(40, len(" DETAIL INFORMASI "), len(title) + 2, max_line + 2)
            inner_w = min(inner_w, 80)

            result += border(inner_w, "=")
            result += center_line(" DETAIL INFORMASI ", inner_w)
            result += border(inner_w, "=") + "\n"

            result += border(inner_w, "-")
            result += center_line(f" {title} ", inner_w)
            result += border(inner_w, "-")

            for l in lines:
                result += "|" + f" {l}".ljust(inner_w - 1) + "|\n"

            result += border(inner_w, "-") + "\n"

        return result
