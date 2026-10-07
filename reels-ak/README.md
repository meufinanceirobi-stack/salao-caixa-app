# Reels AK · "Você sabe quanto ganha de verdade?"

- `AK-reels-diagnostico.mp4`: vídeo pronto (1080×1920, 25s, 30fps, com trilha).
- `ak-reels.html`: a mesma animação no navegador. Abra no Google Chrome do computador e clique em **Baixar MP4**.
- `src/`: arquivos-fonte (`ak-reels.template.html` + logo + fonte Montserrat/OFL).
  - `python3 src/build.py` gera o `ak-reels.html`.
  - `node src/render.mjs ak-reels.html saida.mp4 <ffmpeg>` gera o MP4 quadro a quadro.

## Encerramento "Comenta CLIENTE" (5s)

- `AK-encerramento-cliente.mp4`: final de 5s com logo animada e CTA, para colar no fim de qualquer Reels.
- `ak-encerramento.html`: a mesma animação, com o botão **Baixar MP4**.
- Fonte: `src/ak-encerramento.template.html` → `python3 src/build.py ak-encerramento`.

## Post 10/10 "Falta de sorte é falta de rotina" (22s, 4:5)

- `AK-post-10-10.mp4`: vídeo 1080×1350 para o feed, com trilha.
- `ak-post-10-10.html`: a mesma animação, com o botão **Baixar MP4**.
- Fonte: `src/ak-post-10-10.template.html` → `python3 src/build.py ak-post-10-10`.
- `AK-post-10-10-reels-completo.mp4`: versão vertical (9:16) do post + encerramento "Comenta RAIO-X" (≈41s).
- `AK-encerramento-raiox.mp4` / `ak-encerramento-raiox.html`: encerramento de 7s "Comenta RAIO-X".
- O post tem pausas de leitura (`HOLDS` em `src/ak-post-10-10.template.html`); o fundo e a música seguem no tempo real.
