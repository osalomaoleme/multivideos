@echo off
setlocal EnableDelayedExpansion

title Multi Videos - Verificando dependencias

echo ============================================
echo   Multi Videos - por Salomao Leme
echo ============================================
echo.

REM Verifica se FFmpeg esta instalado
where ffmpeg >nul 2>&1
if %errorlevel% equ 0 (
    echo FFmpeg ja esta instalado.
    goto :run_app
)

echo FFmpeg nao encontrado. Baixando...
echo.

REM Verifica se ja foi baixado anteriormente
if exist "ffmpeg\bin\ffmpeg.exe" (
    echo FFmpeg ja foi baixado anteriormente.
    goto :add_path
)

REM Cria pasta temporaria
if not exist "temp" mkdir temp

echo Baixando FFmpeg (pode levar alguns minutos)...
echo.

REM URL do FFmpeg (versao full build compactada)
set "ffmpeg_url=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
set "zip_file=temp\ffmpeg.zip"

REM Baixa FFmpeg
powershell -Command "Invoke-WebRequest -Uri '%ffmpeg_url%' -OutFile '%zip_file%'"

if not exist "%zip_file%" (
    echo Erro ao baixar FFmpeg. Verifique sua conexao.
    pause
    exit /b 1
)

echo Extraindo arquivos...
powershell -Command "Expand-Archive -Path '%zip_file%' -DestinationPath 'temp' -Force"

REM Localiza a pasta bin do FFmpeg
for /d %%i in (temp\ffmpeg-*) do (
    set "ffmpeg_dir=%%i"
)

if not defined ffmpeg_dir (
    echo Erro ao localizar arquivos do FFmpeg.
    pause
    exit /b 1
)

echo Movendo arquivos...
move "%ffmpeg_dir%\bin" "ffmpeg" >nul 2>&1
move "%ffmpeg_dir%\doc" "ffmpeg" >nul 2>&1

REM Limpa arquivos temporarios
rmdir /s /q "temp" 2>nul
rmdir /s /q "%ffmpeg_dir%" 2>nul
del "%zip_file%" 2>nul

if not exist "ffmpeg\bin\ffmpeg.exe" (
    echo Erro ao configurar FFmpeg.
    pause
    exit /b 1
)

echo FFmpeg baixado com sucesso!
echo.

:add_path
REM Adiciona FFmpeg ao PATH temporariamente
set "PATH=%CD%\ffmpeg\bin;%PATH%"

:run_app
REM Adiciona FFmpeg ao PATH e executa o app
set "PATH=%CD%\ffmpeg\bin;%PATH%"

echo Iniciando Multi Videos...
echo.
start "" "MultiVideos.exe"
exit
