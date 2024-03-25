import locale


class Line:
    """
    Line of Edax' output.

    Attributes:
        string: Original string.
        index: Index of the position.
        depth: Depth of the search.
        selectivity: Selectivity in percentage.
        score: Score of the position.
        time: Time taken to search.
        nodes: Number of nodes searched.
        nodes_per_second: Nodes per second of the search.
        pv: Principal variation line.
    """

    def __init__(self, string: str):
        self.string = string

        index, rest = string.split("|")

        self.index = int(index)

        intensity = rest[:6].strip()
        self.selectivity: int | None
        if "@" in intensity:
            depth, selectivity = intensity.split("@")
            self.depth = int(depth)
            self.selectivity = int(selectivity[:-1])
        else:
            self.depth = int(intensity)
            self.selectivity = None

        self.score = int(rest[7:12].strip())
        self.time = rest[13:27].strip()
        self.nodes = int(rest[28:41].strip())

        nodes_per_second = rest[42:52].strip()
        self.nodes_per_second = int(nodes_per_second) if nodes_per_second else None

        pv = rest[53:73].split()
        self.pv = [x for x in pv if x != ""]

    def __str__(self) -> str:
        return self.string

    def pretty_string(self) -> str:
        "Returns a pretty string."
        locale.setlocale(locale.LC_ALL, "")
        if self.nodes_per_second is not None:
            nodes_per_second = f"{self.nodes_per_second:n} N/s"
        else:
            nodes_per_second = "? N/s"
        pv = " ".join(self.pv)
        return "\n".join(
            [
                f"index: {self.index}",
                f"depth: {self.depth}",
                f"selectivity: {self.selectivity}%",
                f"score: {self.score:+03}",
                f"time: {self.time}",
                f"nodes: {self.nodes:n}",
                f"nodes_per_second: {nodes_per_second:n}",
                f"pv: {pv}",
            ]
        )


class Output:
    """
    Output of Edax' search.
    Attributes:
        string: Original string.
        lines: List of lines.
        nodes: Number of nodes searched.
        time: Time taken to search.
        nodes_per_second: Nodes per second of the search.
    """

    def __init__(self, string: str):
        self.string = string

        lines = string.split("\n")
        summary = lines[-3].split()

        self.lines = [Line(line) for line in lines[2:-4]]
        self.nodes = int(summary[1])
        self.time = summary[4]

        nps = None
        if len(summary) > 5:
            if summary[5] == "(":
                nps = int(summary[6])
            else:
                nps = int(summary[5][1:])
        self.nodes_per_second = nps
