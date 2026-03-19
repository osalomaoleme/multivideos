#!/usr/bin/env python3
"""
YouTube Video Downloader — Desktop App
Interface gráfica moderna com customtkinter + yt-dlp.
"""

import customtkinter as ctk
import yt_dlp
import os
import sys
import threading
import webbrowser
from tkinter import filedialog, messagebox


# ──────────────────────────────────────────────
#  Tema e Cores
# ──────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Paleta de cores
COR_BG_PRINCIPAL = "#0f0f0f"       # Fundo principal (preto YouTube)
COR_BG_CARD = "#1a1a2e"            # Fundo dos cards
COR_BG_CARD_HOVER = "#16213e"      # Card hover
COR_ACCENT = "#FF0033"             # Vermelho YouTube
COR_ACCENT_HOVER = "#CC0029"       # Vermelho escuro hover
COR_ACCENT_LIGHT = "#FF4D6A"       # Vermelho claro
COR_TEXT = "#FFFFFF"               # Texto principal
COR_TEXT_SEC = "#8E8E93"           # Texto secundário
COR_INPUT_BG = "#1C1C1E"          # Fundo inputs
COR_INPUT_BORDER = "#2C2C2E"      # Borda inputs
COR_SUCCESS = "#30D158"           # Verde sucesso
COR_ERROR = "#FF453A"             # Vermelho erro
COR_PROGRESS_BG = "#2C2C2E"      # Fundo barra de progresso


# ──────────────────────────────────────────────
#  Formatos disponíveis
# ──────────────────────────────────────────────
FORMATOS = {
    "🎥 Melhor Qualidade (MP4)": {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
    },
    "🎥 1080p (MP4)": {
        "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best",
        "merge_output_format": "mp4",
    },
    "🎥 720p (MP4)": {
        "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "merge_output_format": "mp4",
    },
    "🎥 480p (MP4)": {
        "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best",
        "merge_output_format": "mp4",
    },
    "🎵 Áudio MP3 (320kbps)": {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
    },
    "🎵 Áudio M4A (256kbps)": {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "256",
        }],
    },
}


# ──────────────────────────────────────────────
#  Aplicação Principal
# ──────────────────────────────────────────────
class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # -- Janela --
        self.title("Multi Videos")
        self.geometry("650x700")
        self.resizable(True, True)
        self.minsize(550, 600)
        self.configure(fg_color=COR_BG_PRINCIPAL)

        # Centralizar na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (650 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"650x700+{x}+{y}")

        # Estado
        self.downloading = False
        self.pasta_destino = os.path.join(os.path.expanduser("~"), "Downloads")

        # Rodape FIXO na parte inferior da janela (fora das abas)
        self._criar_footer()

        # Tabs
        self.tabview = ctk.CTkTabview(self, fg_color="transparent")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10, 0))
        self.tab_main = self.tabview.add("Baixar")
        self.tab_sobre = self.tabview.add("Sobre & Licenca")

        # Construir UI Principal
        self._criar_header(self.tab_main)
        self._criar_campo_url(self.tab_main)
        self._criar_campo_pasta(self.tab_main)
        self._criar_campo_formato(self.tab_main)
        self._criar_botao_download(self.tab_main)
        self._criar_area_status(self.tab_main)

        # Construir Aba Sobre
        self._criar_aba_sobre()

    # ── Header ──────────────────────────────────

    def _criar_header(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(15, 5))

        titulo = ctk.CTkLabel(
            header,
            text="Baixar Videos",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=COR_TEXT,
        )
        titulo.pack(anchor="w")

        subtitulo = ctk.CTkLabel(
            header,
            text="YouTube, Instagram, Facebook, TikTok, X e LinkedIn",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=COR_TEXT_SEC,
        )
        subtitulo.pack(anchor="w", pady=(2, 0))

        # Linha separadora estilizada
        sep = ctk.CTkFrame(parent, height=2, fg_color=COR_ACCENT, corner_radius=1)
        sep.pack(fill="x", padx=10, pady=(12, 0))

    # ── Campo URL ───────────────────────────────

    def _criar_campo_url(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=COR_BG_CARD, corner_radius=12, border_width=1,
            border_color=COR_INPUT_BORDER
        )
        card.pack(fill="x", padx=10, pady=(20, 0))

        label = ctk.CTkLabel(
            card,
            text="🔗  URL do Vídeo",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COR_TEXT,
        )
        label.pack(anchor="w", padx=16, pady=(14, 6))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 14))

        self.entry_url = ctk.CTkEntry(
            row,
            placeholder_text="Cole aqui a URL do vídeo...",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=42,
            corner_radius=8,
            fg_color=COR_INPUT_BG,
            border_color=COR_INPUT_BORDER,
            text_color=COR_TEXT,
            placeholder_text_color=COR_TEXT_SEC,
        )
        self.entry_url.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_colar = ctk.CTkButton(
            row,
            text="📋 Colar",
            width=80,
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=COR_INPUT_BORDER,
            hover_color=COR_BG_CARD_HOVER,
            text_color=COR_TEXT,
            command=self._colar_url,
        )
        btn_colar.pack(side="right")

    # ── Campo Pasta ─────────────────────────────

    def _criar_campo_pasta(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=COR_BG_CARD, corner_radius=12, border_width=1,
            border_color=COR_INPUT_BORDER
        )
        card.pack(fill="x", padx=10, pady=(12, 0))

        label = ctk.CTkLabel(
            card,
            text="📂  Salvar em",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COR_TEXT,
        )
        label.pack(anchor="w", padx=16, pady=(14, 6))

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=(0, 14))

        self.label_pasta = ctk.CTkLabel(
            row,
            text=self.pasta_destino,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COR_TEXT_SEC,
            anchor="w",
            height=42,
            corner_radius=8,
            fg_color=COR_INPUT_BG,
        )
        self.label_pasta.pack(side="left", fill="x", expand=True, padx=(0, 8), ipadx=10)

        btn_pasta = ctk.CTkButton(
            row,
            text="📁 Procurar",
            width=100,
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=COR_INPUT_BORDER,
            hover_color=COR_BG_CARD_HOVER,
            text_color=COR_TEXT,
            command=self._escolher_pasta,
        )
        btn_pasta.pack(side="right")

    # ── Campo Formato ───────────────────────────

    def _criar_campo_formato(self, parent):
        card = ctk.CTkFrame(
            parent, fg_color=COR_BG_CARD, corner_radius=12, border_width=1,
            border_color=COR_INPUT_BORDER
        )
        card.pack(fill="x", padx=10, pady=(12, 0))

        label = ctk.CTkLabel(
            card,
            text="🎬  Formato",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COR_TEXT,
        )
        label.pack(anchor="w", padx=16, pady=(14, 6))

        self.combo_formato = ctk.CTkComboBox(
            card,
            values=list(FORMATOS.keys()),
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=42,
            corner_radius=8,
            fg_color=COR_INPUT_BG,
            border_color=COR_INPUT_BORDER,
            button_color=COR_ACCENT,
            button_hover_color=COR_ACCENT_HOVER,
            dropdown_fg_color=COR_BG_CARD,
            dropdown_hover_color=COR_ACCENT,
            dropdown_text_color=COR_TEXT,
            text_color=COR_TEXT,
            state="readonly",
        )
        self.combo_formato.set(list(FORMATOS.keys())[0])
        self.combo_formato.pack(fill="x", padx=16, pady=(0, 14))

    # ── Botão Download ──────────────────────────

    def _criar_botao_download(self, parent):
        self.btn_download = ctk.CTkButton(
            parent,
            text="⬇️  BAIXAR VÍDEO",
            height=50,
            corner_radius=12,
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            fg_color=COR_ACCENT,
            hover_color=COR_ACCENT_HOVER,
            text_color=COR_TEXT,
            command=self._iniciar_download,
        )
        self.btn_download.pack(fill="x", padx=10, pady=(20, 0))

    # ── Área de Status ──────────────────────────

    def _criar_area_status(self, parent):
        status_frame = ctk.CTkFrame(parent, fg_color="transparent")
        status_frame.pack(fill="x", padx=10, pady=(16, 20))

        self.progress_bar = ctk.CTkProgressBar(
            status_frame,
            height=8,
            corner_radius=4,
            fg_color=COR_PROGRESS_BG,
            progress_color=COR_ACCENT,
        )
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)

        self.label_status = ctk.CTkLabel(
            status_frame,
            text="Pronto para baixar",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COR_TEXT_SEC,
            anchor="w",
        )
        self.label_status.pack(anchor="w", pady=(8, 0))

        self.label_detalhes = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COR_TEXT_SEC,
            anchor="w",
        )
        self.label_detalhes.pack(anchor="w", pady=(2, 0))

    # ── Aba Sobre & Licença ─────────────────────

    def _criar_aba_sobre(self):
        container = ctk.CTkFrame(self.tab_sobre, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_titulo = ctk.CTkLabel(
            container, text="Baixar Videos",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=COR_TEXT,
        )
        lbl_titulo.pack(pady=(20, 2))

        lbl_versao = ctk.CTkLabel(
            container, text="v1.0  |  Codigo Aberto  |  100% Gratuito",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COR_ACCENT_LIGHT,
        )
        lbl_versao.pack(pady=(0, 15))

        # Card ─ Licença
        card_lic = ctk.CTkFrame(
            container, fg_color=COR_BG_CARD, corner_radius=12,
            border_width=1, border_color=COR_INPUT_BORDER
        )
        card_lic.pack(fill="x", pady=(0, 10))

        lbl_lic_titulo = ctk.CTkLabel(
            card_lic, text="📜  Licença de Uso",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COR_TEXT, anchor="w",
        )
        lbl_lic_titulo.pack(anchor="w", padx=16, pady=(14, 6))

        lbl_lic_texto = ctk.CTkLabel(
            card_lic,
            text=(
                "Este software é gratuito e de código aberto.\n"
                "Sua venda ou comercialização é estritamente proibida.\n"
                "Modificações são permitidas desde que os créditos\n"
                "ao autor original sejam mantidos."
            ),
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COR_TEXT_SEC, justify="left", anchor="w",
        )
        lbl_lic_texto.pack(anchor="w", padx=16, pady=(0, 14))

        # Card ─ Autor
        card_autor = ctk.CTkFrame(
            container, fg_color=COR_BG_CARD, corner_radius=12,
            border_width=1, border_color=COR_INPUT_BORDER
        )
        card_autor.pack(fill="x", pady=(0, 10))

        lbl_autor_titulo = ctk.CTkLabel(
            card_autor, text="👨‍💻  Desenvolvedor",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COR_TEXT, anchor="w",
        )
        lbl_autor_titulo.pack(anchor="w", padx=16, pady=(14, 6))

        lbl_autor_nome = ctk.CTkLabel(
            card_autor,
            text="Salomão Leme",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=COR_ACCENT_LIGHT, anchor="w",
        )
        lbl_autor_nome.pack(anchor="w", padx=16, pady=(0, 4))

        lbl_autor_desc = ctk.CTkLabel(
            card_autor,
            text="Projeto open-source feito no Brasil.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COR_TEXT_SEC, anchor="w",
        )
        lbl_autor_desc.pack(anchor="w", padx=16, pady=(0, 14))

        # Card ─ Aviso legal
        card_aviso = ctk.CTkFrame(
            container, fg_color=COR_BG_CARD, corner_radius=12,
            border_width=1, border_color=COR_INPUT_BORDER
        )
        card_aviso.pack(fill="x", pady=(0, 10))

        lbl_aviso_titulo = ctk.CTkLabel(
            card_aviso, text="⚠️  Aviso Legal",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color=COR_TEXT, anchor="w",
        )
        lbl_aviso_titulo.pack(anchor="w", padx=16, pady=(14, 6))

        lbl_aviso_texto = ctk.CTkLabel(
            card_aviso,
            text=(
                "Software fornecido \"como está\", sem garantias.\n"
                "O autor não se responsabiliza por danos\n"
                "decorrentes do uso deste programa."
            ),
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=COR_TEXT_SEC, justify="left", anchor="w",
        )
        lbl_aviso_texto.pack(anchor="w", padx=16, pady=(0, 14))

    # ── Rodapé (Footer) ─────────────────────────

    def _abrir_link(self, url):
        webbrowser.open(url)

    def _criar_footer(self):
        footer = ctk.CTkFrame(self, fg_color=COR_BG_CARD, height=55, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        inner = ctk.CTkFrame(footer, fg_color="transparent")
        inner.pack(expand=True)

        lbl_siga = ctk.CTkLabel(
            inner, text="Siga-me nas redes sociais:",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=COR_TEXT_SEC,
        )
        lbl_siga.pack(side="left", padx=(0, 8))

        redes = [
            ("X",  "https://x.com/osalomaoleme",                              "#1DA1F2"),
            ("Li", "https://www.linkedin.com/in/osalomaoleme/",                "#0A66C2"),
            ("Fb", "https://www.facebook.com/profile.php?id=61556186734919",   "#1877F2"),
            ("Yt", "https://www.youtube.com/@osalomaoleme",                    "#FF0000"),
            ("Ig", "https://www.instagram.com/osalomaoleme/",                  "#E1306C"),
            ("Tk", "https://www.tiktok.com/@osalomaoleme",                     "#EEEEEE"),
        ]

        for sigla, url, cor in redes:
            btn = ctk.CTkButton(
                inner, text=sigla, width=34, height=26,
                corner_radius=6,
                fg_color=COR_INPUT_BORDER,
                hover_color=cor,
                text_color=cor,
                font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
                command=lambda u=url: self._abrir_link(u),
            )
            btn.pack(side="left", padx=2)

        lbl_sep = ctk.CTkLabel(
            inner, text="|",
            font=ctk.CTkFont(size=14),
            text_color=COR_INPUT_BORDER,
        )
        lbl_sep.pack(side="left", padx=(8, 8))

        lbl_dev = ctk.CTkLabel(
            inner, text="por Salomao Leme",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=COR_TEXT_SEC,
        )
        lbl_dev.pack(side="left")

    # ──────────────────────────────────────────────
    #  Ações
    # ──────────────────────────────────────────────

    def _colar_url(self):
        """Cola o conteúdo da área de transferência no campo de URL."""
        try:
            texto = self.clipboard_get()
            self.entry_url.delete(0, "end")
            self.entry_url.insert(0, texto.strip())
        except Exception:
            pass

    def _escolher_pasta(self):
        """Abre o diálogo do Windows para escolher a pasta de destino."""
        pasta = filedialog.askdirectory(
            title="Escolher pasta de destino",
            initialdir=self.pasta_destino,
        )
        if pasta:
            self.pasta_destino = pasta
            self.label_pasta.configure(text=pasta)

    def _validar_url(self, url):
        """Verifica se a URL parece ser suportada."""
        dominios = [
            "youtube.com", "youtu.be", "www.youtube.com", "m.youtube.com", "music.youtube.com",
            "instagram.com", "www.instagram.com",
            "facebook.com", "www.facebook.com", "fb.watch",
            "tiktok.com", "www.tiktok.com", "vm.tiktok.com", "vt.tiktok.com",
            "twitter.com", "x.com",
            "linkedin.com", "www.linkedin.com"
        ]
        return any(d in url for d in dominios)

    def _atualizar_status(self, texto, cor=None):
        """Atualiza o label de status na thread principal."""
        if cor:
            self.label_status.configure(text=texto, text_color=cor)
        else:
            self.label_status.configure(text=texto)

    def _atualizar_detalhes(self, texto):
        """Atualiza o label de detalhes."""
        self.label_detalhes.configure(text=texto)

    def _iniciar_download(self):
        """Valida inputs e inicia o download em uma thread separada."""
        if self.downloading:
            return

        url = self.entry_url.get().strip()

        if not url:
            messagebox.showwarning("Atenção", "Cole uma URL de vídeo no campo acima.")
            return

        if not self._validar_url(url):
            messagebox.showerror("URL Inválida", "URL não suportada.\nCole uma URL válida (YouTube, Instagram, Facebook, TikTok, X ou LinkedIn).")
            return

        # Iniciar download em thread separada
        self.downloading = True
        self.btn_download.configure(
            text="⏳  BAIXANDO...",
            fg_color=COR_TEXT_SEC,
            state="disabled",
        )
        self.progress_bar.set(0)
        self._atualizar_status("🔍 Obtendo informações do vídeo...", COR_TEXT_SEC)
        self._atualizar_detalhes("")

        thread = threading.Thread(target=self._executar_download, args=(url,), daemon=True)
        thread.start()

    def _executar_download(self, url):
        """Executa o download (roda em thread separada)."""
        formato_nome = self.combo_formato.get()
        formato_config = FORMATOS[formato_nome]

        def hook_progresso(d):
            if d["status"] == "downloading":
                # Extrair porcentagem
                percent_str = d.get("_percent_str", "0%").strip()
                try:
                    percent = float(percent_str.replace("%", "")) / 100.0
                except ValueError:
                    percent = 0.0

                speed = d.get("_speed_str", "-- B/s").strip()
                eta = d.get("_eta_str", "--:--").strip()

                self.after(0, lambda p=percent: self.progress_bar.set(p))
                self.after(0, lambda: self._atualizar_status(
                    f"⬇️  Baixando... {percent_str}", COR_ACCENT_LIGHT
                ))
                self.after(0, lambda s=speed, e=eta: self._atualizar_detalhes(
                    f"Velocidade: {s}  •  Tempo restante: {e}"
                ))

            elif d["status"] == "finished":
                self.after(0, lambda: self.progress_bar.set(1.0))
                self.after(0, lambda: self._atualizar_status(
                    "⚙️  Processando arquivo...", COR_TEXT_SEC
                ))
                self.after(0, lambda: self._atualizar_detalhes(""))

        # Montar opções do yt-dlp
        opcoes = {
            "outtmpl": os.path.join(self.pasta_destino, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "nocheckcertificate": True,
            "progress_hooks": [hook_progresso],
            **formato_config,
        }

        try:
            with yt_dlp.YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=False)
                titulo = info.get("title", "Vídeo")

                self.after(0, lambda t=titulo: self._atualizar_status(
                    f"⬇️  Baixando: {t[:45]}...", COR_ACCENT_LIGHT
                ))

                ydl.download([url])

            # Sucesso
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.after(0, lambda: self._atualizar_status(
                f"✅  Download concluído!", COR_SUCCESS
            ))
            self.after(0, lambda: self._atualizar_detalhes(
                f"Salvo em: {self.pasta_destino}"
            ))

        except yt_dlp.utils.DownloadError as e:
            erro = str(e)
            self.after(0, lambda: self.progress_bar.set(0))
            self.after(0, lambda: self._atualizar_status(
                f"❌  Erro no download", COR_ERROR
            ))
            self.after(0, lambda err=erro: self._atualizar_detalhes(err))

        except Exception as e:
            erro = str(e)
            self.after(0, lambda: self.progress_bar.set(0))
            self.after(0, lambda: self._atualizar_status(
                f"❌  Erro inesperado", COR_ERROR
            ))
            self.after(0, lambda err=erro: self._atualizar_detalhes(err))

        finally:
            self.after(0, self._resetar_botao)

    def _resetar_botao(self):
        """Restaura o botão de download ao estado original."""
        self.downloading = False
        self.btn_download.configure(
            text="⬇️  BAIXAR VÍDEO",
            fg_color=COR_ACCENT,
            state="normal",
        )


# ──────────────────────────────────────────────
#  Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
