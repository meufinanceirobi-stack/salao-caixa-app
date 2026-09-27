# Reels AK · "Você sabe quanto ganha de verdade?"

- `AK-reels-diagnostico.mp4`: vídeo pronto (1080×1920, 25s, 30fps, com trilha).
- `ak-reels.html`: a mesma animação no navegador. Abra no Google Chrome do computador e clique em **Baixar MP4**.
- `src/`: arquivos-fonte (`ak-reels.template.html` + logo + fonte Montserrat/OFL).
  - `python3 src/build.py` gera o `ak-reels.html`.
  - `node src/render.mjs ak-reels.html saida.mp4 <ffmpeg>` gera o MP4 quadro a quadro.
