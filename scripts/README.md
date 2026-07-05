# Scripts

## Lancer un script
Toutes les instructions sont à lancer depuis la racine.

Exemple avec Qwen 7B, quantification `q5_k_m`, script `run_agent_read.py`.

Ouvrir un terminal et lancer la connexion au serveur
```
./third_party/llama.cpp/build/bin/llama-server \
    -m models/qwen7b/qwen2.5-coder-7b-instruct-q5_k_m.gguf \
    --jinja
```

Ouvrir un autre terminal et lancer le script
```
python scripts/run_agent_read.py
```

## Liste des scripts et fonctionnalités

| Scripts | Fonctionnalité |
|-----|-----|
| `run_agent_read.py` | Lecture de fichier |
| `run_agent_write.py` | Écriture de fichier |