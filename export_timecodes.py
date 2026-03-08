import reapy_boost as rpr


class Timecode:
    def __init__(
        self, time_in_secs: float, time_selection: rpr.TimeSelection, name: str
    ):
        self.time = time_in_secs - time_selection.start
        self.name = name


def build_timecodes():
    pr = rpr.Project()
    ts = pr.time_selection
    # print(ts.start, ts.end)
    timecodes = [Timecode(ts.start, ts, "Вступление")]
    for marker in pr.markers:
        timecodes.append(Timecode(marker.position, ts, marker.name))
    return timecodes


if __name__ == "__main__":
    for timecode in build_timecodes():
        h = int(timecode.time // 3600)
        m = int((timecode.time % 3600) // 60)
        s = int(timecode.time % 60)
        print(f"{h:02}:{m:02}:{s:02} ‒ {timecode.name}")
