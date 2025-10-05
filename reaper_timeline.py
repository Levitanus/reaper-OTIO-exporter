from pathlib import Path
from typing import TypedDict
import reapy_boost as rpr
from pprint import pprint, pformat


class ReaperTimeLine(TypedDict):
    start: float
    length: float
    tracks: dict[str, list["ReaperItem"]]


def build_timeline() -> ReaperTimeLine:
    pr = rpr.Project()
    ts = pr.time_selection
    tracks: dict[str, list[ReaperItem]] = {}
    tl_start = None
    tl_end = None
    audio_file = rpr.Project().get_info_string("RENDER_TARGETS").split(";")[0]
    print(audio_file)
    tracks["audio"] = [ReaperItem(audio_file, 0.0, 0.0, ts.length, False)]

    for track_nr, track in enumerate(reversed(pr.tracks)):
        track_key = f"{track_nr} {track.name}" or str(track_nr)
        for item_idx, item in enumerate(track.items):
            if item.get_info_value("B_MUTE"):
                continue
            take = item.active_take
            source = take.source
            if source.type == "VIDEO":
                position = item.position
                length = item.length
                if position >= ts.end:
                    continue
                if position + length <= ts.start:
                    continue
                # print(item_idx, take.name, position, item.length, item.track.name)
                start_offset = take.start_offset
                end = position + length
                if round(position, 5) < round(ts.start, 5):
                    diff = ts.start - position
                    position = ts.start
                    start_offset += diff
                end = min(end, ts.end)
                length = end - position
                filename = source.filename
                if tl_start is None or round(tl_start, 5) > round(position, 5):
                    print(
                        f"tl start: {tl_start}, position: {position}, item: {take.name}"
                    )
                    tl_start = position
                if tl_end is None or round(tl_end, 5) < round(end, 5):
                    tl_end = end

                if track_key in tracks:
                    tr = tracks[track_key]
                else:
                    tr = []
                    tracks[track_key] = tr
                tr.append(
                    ReaperItem(
                        filename,
                        start_offset,
                        position,
                        length,
                        bool(item.get_info_value("B_MUTE")),
                    )
                )
    if tl_end is None or tl_start is None:
        length = 0.0
        start = 0.0
    else:
        length = tl_end - tl_start
        start = tl_start
    diff = start
    print(f"tl start diff: {diff}")
    start = 0
    length = length - diff
    for track in tracks.values():
        for item in track:
            item.position -= diff
    return {"start": start, "length": length, "tracks": tracks}


class ReaperItem:
    def __init__(
        self,
        filename: str,
        start_offset: float,
        position: float,
        length: float,
        muted: bool,
    ):
        self.filename: Path = Path(filename)
        self.start_offset = start_offset
        self.position = position
        self.length = length
        self.enabled = not muted

    def __repr__(self):
        return f"Clip at {id(self)}:\
                \n{pformat(vars(self), indent=4)}"

    @property
    def end(self) -> float:
        return self.position + self.length


if __name__ == "__main__":
    with rpr.inside_reaper():
        pprint(build_timeline())
