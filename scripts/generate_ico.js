import { Jimp } from 'jimp';
import toIco from 'to-ico';
import fs from 'fs';
import path from 'path';

async function generateIcons() {
  const sourceImagePath = path.resolve('src/assets/images/matrical_app_icon_1786598955535.jpg');
  console.log('Loading image from:', sourceImagePath);

  const image = await Jimp.read(sourceImagePath);

  // Generate PNG buffers for standard Windows ICO icon sizes
  const sizes = [16, 24, 32, 48, 64, 128, 256];
  const pngBuffers = [];

  for (const size of sizes) {
    const resized = image.clone().resize({ w: size, h: size });
    const buffer = await resized.getBuffer('image/png');
    pngBuffers.push(buffer);
  }

  // Write public/icon.png & src/assets/logo.png
  const image256 = image.clone().resize({ w: 256, h: 256 });
  await image256.write(path.resolve('public/icon.png'));
  await image256.write(path.resolve('src/assets/logo.png'));

  console.log('Generating valid Windows ICO file with to-ico...');
  const icoBuffer = await toIco(pngBuffers, { resize: false });

  fs.writeFileSync(path.resolve('icon.ico'), icoBuffer);
  fs.writeFileSync(path.resolve('public/icon.ico'), icoBuffer);
  fs.writeFileSync(path.resolve('public/favicon.ico'), icoBuffer);

  console.log('Successfully generated Windows ICO icon (size:', icoBuffer.length, 'bytes)!');
}

generateIcons().catch((err) => {
  console.error('Error generating icons:', err);
  process.exit(1);
});

