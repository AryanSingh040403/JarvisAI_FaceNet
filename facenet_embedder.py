# facenet_embedder.py
import torch
from facenet_pytorch import InceptionResnetV1
from torchvision import transforms
from PIL import Image
import numpy as np
from pathlib import Path

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Model: InceptionResnetV1 pretrained on vggface2 -> 512-D embeddings
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

transform = transforms.Compose([
    transforms.Resize((160,160)),
    transforms.ToTensor(),
    transforms.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5])
])

def image_to_embedding(img_path: str):
    img = Image.open(img_path).convert('RGB')
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = model(x)
    return emb.cpu().numpy().flatten()

def save_embeddings(name: str, embeddings, paths, out_dir='embeddings'):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    np.savez_compressed(Path(out_dir) / f"{name}.npz", embeddings=embeddings, paths=np.array(paths))

def load_embeddings(npzfile: str):
    d = np.load(npzfile, allow_pickle=True)
    return d['embeddings'], d['paths']
