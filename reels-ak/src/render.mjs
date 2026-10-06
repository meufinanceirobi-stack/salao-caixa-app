// Gera o MP4: desenha cada quadro com render(t) e junta com a trilha (OfflineAudioContext).
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const [, , htmlPath, outPath, ffmpeg, onlyFrames] = process.argv;
const FPS = 30;
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--autoplay-policy=no-user-gesture-required'] });
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
page.on('console', m => console.log('page:', m.text()));
page.on('pageerror', e => console.log('ERR', e.message));
await page.goto('file://' + path.resolve(htmlPath));
await page.waitForFunction(() => window.__ready === true, null, { timeout: 60000 });
const DUR = await page.evaluate(() => DUR);
if (onlyFrames) { // imagens de conferência
  for (const t of onlyFrames.split(',').map(Number)) {
    const b64 = await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', .85).split(',')[1]; }, t);
    fs.writeFileSync(`${outPath}/f_${String(t).padStart(5, '0')}.jpg`, Buffer.from(b64, 'base64'));
  }
  await browser.close(); process.exit(0);
}
const wav = await page.evaluate(() => renderAudioWav());
const wavPath = outPath + '.wav'; fs.writeFileSync(wavPath, Buffer.from(wav, 'base64'));
const ff = spawn(ffmpeg, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-i', wavPath,
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-maxrate', '8M', '-bufsize', '16M', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', String(FPS),
  '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', '-shortest', outPath], { stdio: ['pipe', 'inherit', 'inherit'] });
const N = FPS * DUR, t0 = Date.now();
for (let i = 0; i < N; i++) {
  const b64 = await page.evaluate(t => { render(t); return document.getElementById('c').toDataURL('image/jpeg', .96).split(',')[1]; }, i / FPS);
  if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  if (i % 75 === 0) console.log(`quadro ${i}/${N} (${((Date.now() - t0) / 1000).toFixed(0)}s)`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
fs.unlinkSync(wavPath);
await browser.close();
console.log('MP4 pronto:', outPath);
