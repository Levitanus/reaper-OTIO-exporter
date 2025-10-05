import librosa as lr
import reapy_boost as rpr
from pathlib import Path
from scipy import signal
import numpy as np
from pprint import pprint

pr = rpr.Project()

items = [item for item in pr.selected_items]
print([item.active_take.source.filename for item in items])
print("loading ref")
SR = 22050
ref, sr = lr.load(items[0].active_take.source.filename, sr=SR, mono=True)
# ref_s = lr.feature.melspectrogram(y=ref, sr=SR)

for idx, item in enumerate(items[1:]):
    file = Path(item.active_take.source.filename)
    print(f"loading file {file}")
    target, sr = lr.load(file, sr=SR, mono=True, duration=300)
    # s = lr.feature.melspectrogram(y=ref, sr=SR)
    # pprint([ref, rms])
    c = signal.correlate(ref, target, mode='valid', method='fft')
    print(c)
    peak = np.argmax(c)
    print(peak)
    offset = lr.samples_to_time(peak, sr=SR)
    # offset = round(peak / SR, 2)
    print(offset)
    print(f"{int((idx+2)/len(items)*100)}%")
    item.position = float(offset)
    del target, c

