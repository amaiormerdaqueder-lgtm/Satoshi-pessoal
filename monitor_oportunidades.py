

import json
import os
from datetime import datetime, timezone
from urllib.request import Request, urlopen

FONTES = [
    {
        "nome": "Bitcoin",
        "url": "https://www.reddit.com/r/beermoney/search.json?q=paid+surveys+bitcoin&restrict_sr=1&sort=new&limit=10"
    },
    {
        "nome": "Microtarefas",
        "url": "https://www.reddit.com/r/beermoney/search.json?q=remote+microtasks+rewards&restrict_sr=1&sort=new&limit=10"
    }
]

def consultar(fonte):
    req = Request(
        fonte["url"],
        headers={"User-Agent": "SatoshiPessoalMonitor/1.0"}
    )
    with urlopen(req, timeout=20) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))

    oportunidades = []
    for item in dados.get("data", {}).get("children", []):
        post = item.get("data", {})
        oportunidades.append({
            "fonte": fonte["nome"],
            "titulo": post.get("title", "Sem título"),
            "link": "https://www.reddit.com" + post.get("permalink", ""),
            "publicado_em": datetime.fromtimestamp(
                post.get("created_utc", 0), timezone.utc
            ).isoformat(),
            "aviso": "Verifique regras, país elegível e reputação antes de participar."
        })
    return oportunidades

def main():
    resultado = {
        "verificado_em": datetime.now(timezone.utc).isoformat(),
        "observacao": (
            "São pistas públicas, não ofertas verificadas. "
            "O monitor não se inscreve nem garante ganhos."
        ),
        "oportunidades": [],
        "erros": []
    }

    for fonte in FONTES:
        try:
            resultado["oportunidades"].extend(consultar(fonte))
        except Exception as erro:
            resultado["erros"].append({
                "fonte": fonte["nome"],
                "erro": str(erro)
            })

    os.makedirs("relatorios", exist_ok=True)
    caminho = "relatorios/oportunidades.json"
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=2)

    print(f"Relatório salvo em {caminho}")
    print(f"Pistas encontradas: {len(resultado['oportunidades'])}")
    print(f"Fontes com erro: {len(resultado['erros'])}")

if __name__ == "__main__":
    main()
