import os
from huggingface_hub import hf_hub_download

def get_model_path():
    """
    Descargar (si no existe) el modelo YOLO desde HuggingFace.
    """
    repo_id = "juancmamacias/detect_logo"  
    filename = "best.pt"                   

    model_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="model",
        token=os.getenv("HF_TOKEN"), 
    )
    return model_path
