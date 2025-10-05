import math
from pathlib import Path
from pprint import pprint

import ffmpeg
import reaper_timeline as rtl
import opentimelineio as otio

FPS = 25
TIME_PRECISION = 5


def seconds_to_frames(seconds: float) -> otio.opentime.RationalTime:
    return otio.opentime.RationalTime(
        rate=FPS,
        value=round(seconds * 25),
        # value=seconds*FPS
    )


def export_time_selection():
    rpr_tl = rtl.build_timeline()
    # pprint(rpr_tl)
    tl = otio.schema.Timeline(
        name="test timeline",
        global_start_time=otio.opentime.RationalTime(rate=FPS, value=0),
    )
    for tr_name, track in rpr_tl["tracks"].items():
        # pprint(tr_name)
        if tr_name == "audio":
            kind = otio.schema.TrackKind.Audio
        else:
            kind = otio.schema.TrackKind.Video
        tr = otio.schema.Track(name=tr_name, kind=kind)
        # if track[0].position > 0:
        #     tr.append(
        #         otio.schema.Gap(duration=otio.opentime.from_seconds(track[0].position))
        #     )
        last_end = 0.0
        for i, item in enumerate(track):
            # pprint((i, item))
            # print(i, item.position, last_end)
            if round(last_end, TIME_PRECISION) > round(item.position, TIME_PRECISION):
                item.start_offset += last_end - item.position
                item.length -= last_end - item.position
                item.position = last_end
            if round(item.position, TIME_PRECISION) > round(last_end, TIME_PRECISION):
                print(
                    f"appending gap of length: {item.position - last_end}     - item.position: {item.position}, last_end: {last_end}"
                )
                tr.append(
                    otio.schema.Gap(
                        duration=seconds_to_frames(item.position - last_end)
                    )
                )
            clip = otio.schema.Clip(
                name=f"{item.filename.name} - {i+1}",
                media_reference=otio.schema.ExternalReference(
                    target_url=str(item.filename.absolute()),
                    available_range=get_clip_time_range(item.filename),
                ),
                source_range=otio.opentime.TimeRange(
                    start_time=seconds_to_frames(item.start_offset),
                    duration=seconds_to_frames(item.length),
                ),
                # enabled = item.enabled
            )
            # print(f"clip enabled set to {item.enabled}")
            clip.enabled = item.enabled
            # print(clip.enabled)
            tr.append(clip)
            last_end = item.end
        tl.tracks.append(tr)
    otio.adapters.write_to_file(tl, "test.otio")
    otio.adapters.write_to_file(tl, "test.mlt")
    otio.adapters.write_to_file(tl, "test.kdenlive")


def get_clip_time_range(file: Path) -> otio.opentime.TimeRange:
    try:
        probe = ffmpeg.probe(file.absolute())
    except Exception as e:
        print(f"ffprobe error on file: {file.absolute()}")
        raise e
    video_stream = next(
        (stream for stream in probe["streams"] if stream["codec_type"] == "video"), None
    )
    if video_stream is None:
        video_stream = probe["streams"][0]
    try:
        length = float(video_stream["duration"])
    except KeyError:
        # if no duration in stream, try to get it from format
        length = float(probe["format"]["duration"])
    return otio.opentime.TimeRange(
        start_time=seconds_to_frames(0),
        duration=seconds_to_frames(length),
    )


if __name__ == "__main__":
    import reapy_boost as rpr

    with rpr.inside_reaper():
        export_time_selection()
