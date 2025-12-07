# dataset_capture.py
import cv2
import argparse
from pathlib import Path
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
parser.add_argument('--count', type=int, default=150)
parser.add_argument('--out', default='known_faces')
args = parser.parse_args()

out_dir = Path(args.out) / args.name
out_dir.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(0)
print('Press SPACE to capture; ESC to exit')
collected = 0
while collected < args.count:
    ret, frame = cap.read()
    if not ret:
        break
    disp = frame.copy()
    cv2.putText(disp, f'Images: {collected}/{args.count}', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2.imshow('Capture - press SPACE', disp)
    k = cv2.waitKey(1)
    if k % 256 == 27:
        break
    elif k % 256 == 32:
        p = out_dir / f"{args.name}_{collected:04d}.jpg"
        cv2.imwrite(str(p), frame)
        # augment: flip
        cv2.imwrite(str(out_dir / f"{args.name}_{collected:04d}_f.jpg"), cv2.flip(frame,1))
        # brightness jitter
        m = cv2.convertScaleAbs(frame, alpha=1.0, beta=np.random.randint(-30,30))
        cv2.imwrite(str(out_dir / f"{args.name}_{collected:04d}_b.jpg"), m)
        collected += 1

cap.release()
cv2.destroyAllWindows()
print('Done')
