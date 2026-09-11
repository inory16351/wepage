from pathlib import Path
import subprocess, imageio_ffmpeg
from PIL import Image, ImageDraw
root=Path(__file__).parent/'웹페이지 제작'
out=root/'posters'/'review';out.mkdir(exist_ok=True)
ff=imageio_ffmpeg.get_ffmpeg_exe()
films={'blindtalk':('blind talk to me4_1.mp4',[150,380,650,980,1400,1900]),'inheritance':('유산을 넘겨라, 아니! 신채원.mp4',[100,240,400,560,780,990])}
for slug,(name,times) in films.items():
    sheet=Image.new('RGB',(960,400),'#111111');draw=ImageDraw.Draw(sheet)
    for i,t in enumerate(times):
        dest=out/f'{slug}-{t}.jpg'
        subprocess.run([ff,'-loglevel','error','-y','-ss',str(t),'-i',str(root/'포폴 정리용'/name),'-frames:v','1','-vf','scale=640:-2','-q:v','2',str(dest)],check=True)
        im=Image.open(dest);im.thumbnail((320,180));x=(i%3)*320;y=(i//3)*200
        sheet.paste(im,(x,y));draw.text((x+8,y+181),f'{slug} {t}s',fill='white')
    sheet.save(out/f'{slug}-contact.jpg')
