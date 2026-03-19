@echo off
title Multi Videos - Verificando Ambiente
echo ============================================
echo Multi Videos
echo ============================================
echo.

:: Define o diretório do próprio script como base
set "SCRIPT_DIR=%~dp0"
set "PY_FILE=%SCRIPT_DIR%youtube_downloader.py"

echo Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python nao encontrado. Instale o Python em python.org
    echo.
    pause
    exit /b 1
)
for /f "delims=" %%v in ('python --version 2^>^&1') do echo %%v encontrado.
echo.

echo Verificando FFmpeg...
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg nao encontrado.
    echo.
    set /p "RESPONSE=Deseja instalar o FFmpeg agora? (S/N): "
    if /i "%RESPONSE%"=="S" (
        echo.
        echo Instalando FFmpeg via WinGet...
        winget install --id Gyan.FFmpeg -e --source winget --accept-package-agreements --accept-source-agreements
        if %errorlevel% equ 0 (
            echo FFmpeg instalado com sucesso!
            echo.
            echo IMPORTANTE: Reinicie este script apos a instalacao.
            pause
            exit /b 0
        ) else (
            echo.
            echo Falha ao instalar FFmpeg. Baixe manualmente em: https://www.gyan.dev/ffmpeg/builds/
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo O programa pode nao funcionar sem FFmpeg.
    )
) else (
    echo FFmpeg encontrado.
)
echo.

echo Verificando bibliotecas...
pip show customtkinter >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando customtkinter...
    pip install customtkinter -q
)
pip show yt-dlp >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando yt-dlp...
    pip install yt-dlp -q
)
echo Bibliotecas OK.
echo.

echo Iniciando o programa...
if not exist "%PY_FILE%" (
    echo ERRO: Arquivo nao encontrado: %PY_FILE%
    echo Verifique se o arquivo youtube_downloader.py esta na mesma pasta que este script.
    pause
    exit /b 1
)

python "%PY_FILE%"
if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro ao executar o programa.
    pause
)
exit /b %errorlevel%