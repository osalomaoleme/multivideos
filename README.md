# Multi Videos

Baixe videos publicos do **YouTube**, **Instagram**, **Facebook**, **TikTok**, **X (Twitter)** e **LinkedIn** de forma simples e rapida.

Aplicativo desktop com interface grafica moderna, 100% gratuito e de codigo aberto.

---

## Funcionalidades

- Baixar videos em MP4 (melhor qualidade, 1080p, 720p, 480p)
- Extrair apenas o audio em MP3 (320kbps) ou M4A (256kbps)
- Escolher a pasta de destino para salvar os arquivos
- Barra de progresso em tempo real com velocidade e tempo restante
- Suporte a 6 plataformas: YouTube, Instagram, Facebook, TikTok, X e LinkedIn

---

## Como Usar

### Versao Executavel (Recomendado)

> Nao precisa instalar Python nem nenhuma biblioteca. Basta baixar e rodar.

1. Baixe a pasta **`Versao Executavel`**
2. Execute o arquivo **`iniciar-programa.bat`**
3. Na primeira execucao, o programa ira verificar se voce tem o FFmpeg instalado. Caso nao tenha, ele **baixa e instala automaticamente**
4. O programa abre, cole a URL do video e clique em **Baixar Video**

**Conteudo da pasta:**

```
Versao Executavel/
  MultiVideos.exe        (Programa principal ~25MB)
  iniciar-programa.bat   (Inicializador com verificacao do FFmpeg)
  LICENSE                (Licenca de uso MIT)
```

---

### Versao Script (Para Desenvolvedores)

> Requer Python 3.10+ instalado no computador.

1. Baixe a pasta **`Versao Script`**
2. Execute o arquivo **`iniciar-programa.bat`**
3. O script ira verificar e instalar automaticamente:
   - **Python** (verifica se esta instalado)
   - **FFmpeg** (instala via WinGet se necessario)
   - **customtkinter** (instala via pip)
   - **yt-dlp** (instala via pip)
4. O programa abre automaticamente apos a verificacao

**Conteudo da pasta:**

```
Versao Script/
  youtube_downloader.py    (Codigo fonte em Python)
  iniciar-programa.bat     (Inicializador com verificacao de dependencias)
  LICENSE                  (Licenca de uso MIT)
```

**Ou rode manualmente:**

```bash
pip install customtkinter yt-dlp
python youtube_downloader.py
```

---

## Plataformas Suportadas

| Plataforma | URLs aceitas |
|:---:|:---|
| YouTube | youtube.com, youtu.be, m.youtube.com |
| Instagram | instagram.com (Reels, posts publicos) |
| Facebook | facebook.com, fb.watch |
| TikTok | tiktok.com, vm.tiktok.com |
| X (Twitter) | x.com, twitter.com |
| LinkedIn | linkedin.com (posts publicos) |

> **Importante:** Apenas conteudos publicos podem ser baixados. Videos de contas privadas nao sao acessiveis.

---

## Requisitos do Sistema

- **Windows 10 ou superior**
- **FFmpeg** (instalado automaticamente pelo programa na primeira execucao)
- Conexao com a internet

---

## Tecnologias Utilizadas

- **Python 3** - Linguagem principal
- **customtkinter** - Interface grafica moderna
- **yt-dlp** - Motor de download de videos
- **FFmpeg** - Processamento de audio e video
- **PyInstaller** - Empacotamento do executavel

---

## Licenca

Este projeto esta licenciado sob a **Licenca MIT**.

O uso, modificacao e distribuicao gratuita sao permitidos, desde que os devidos creditos ao autor original sejam mantidos, protegendo os direitos autorais conforme as regras da licenca.

Consulte o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

## Autor

**Salomao Leme**

- [X (Twitter)](https://x.com/osalomaoleme)
- [LinkedIn](https://www.linkedin.com/in/osalomaoleme/)
- [Facebook](https://www.facebook.com/profile.php?id=61556186734919)
- [YouTube](https://www.youtube.com/@osalomaoleme)
- [Instagram](https://www.instagram.com/osalomaoleme/)
- [TikTok](https://www.tiktok.com/@osalomaoleme)
