def interpolation_seq(
    frames: int, peaks: int, frame_1_factor: int = 100, peak_factor: int = 10
):
    peak_step = int((frames-3) / (peaks+1))
    print(peak_step)
    seq = [frame_1_factor]
    seq.append(int(frame_1_factor/100*90))
    seq.append(int(frame_1_factor/100*30))
    seq.append(int(frame_1_factor/100*20))
    for _ in range(peaks):
        for i in range(peak_step):
            if i == 0:
                seq.append(peak_factor)
                continue
            if i == 2:
                seq.append(int(peak_factor/100*80))
                continue
            if i == 4:
                seq.append(int(peak_factor/100*60))
                continue
            seq.append(1)
    return seq

def interpolation_middle_seq(
    frames: int, peaks: int, frame_1_factor: int = 100, peak_factor: int = 10
):
    peak_step = int((frames) / (peaks+1))
    print(peak_step)
    seq = []
    for peak in range(peaks):
        if int(peaks / 2) == peak:
            seq.append(frame_1_factor)
            seq.append(int(frame_1_factor/100*90))
            seq.append(int(frame_1_factor/100*80))
            seq.append(int(frame_1_factor/100*60))
            seq.append(int(frame_1_factor/100*50))
            seq.extend([1]*(peak_step-4))
            continue
        for i in range(peak_step):
            if i == 0:
                seq.append(peak_factor)
                seq.append(int(peak_factor/100*90))
                seq.append(int(peak_factor/100*80))
                seq.append(int(peak_factor/100*70))
                continue
            if i < 3:
                continue
            seq.append(1)
    return seq

print(" ".join([str(i) for i in interpolation_seq(75, 3, peak_factor=15)]))
print(" ".join([str(i) for i in interpolation_middle_seq(75, 3, peak_factor=40)]))
