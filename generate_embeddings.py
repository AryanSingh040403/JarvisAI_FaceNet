# generate_embeddings.py
import argparse
from pathlib import Path
import numpy as np
from facenet_embedder import image_to_embedding, save_embeddings

parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
parser.add_argument('--imgdir', default='known_faces')
parser.add_argument('--out', default='embeddings')
args = parser.parse_args()

imgdir = Path(args.imgdir) / args.name
imgs = sorted(imgdir.glob('*.jpg'))
if not imgs:
    print("No images found in", imgdir)
    raise SystemExit(1)

embs = []
paths = []
for p in imgs:
    emb = image_to_embedding(str(p))
    embs.append(emb)
    paths.append(str(p))

embs = np.vstack(embs)
save_embeddings(args.name, embs, paths, out_dir=args.out)
print('Saved', len(embs), 'embeddings to', Path(args.out) / f"{args.name}.npz")
