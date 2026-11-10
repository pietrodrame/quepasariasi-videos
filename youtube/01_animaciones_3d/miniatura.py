import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
U='/root/.claude/uploads/dbabd36d-2931-58e9-88aa-0e1625a34493/'
S=sys.argv[1]; F=S+'/fonts/Anton.ttf'
W,H=1280,720; GOLD=(242,181,68)

# fondo: frame del reel desenfocado y oscurecido
bg=ImageOps.fit(Image.open(U+'d0f4ab9b-image.png').convert('RGB'),(W,H)).filter(ImageFilter.GaussianBlur(14))
bg=Image.blend(bg,Image.new('RGB',(W,H),(8,10,20)),0.62)

# persona: quitar fondo blanco conectado a los bordes
p=Image.open(U+'e52679cf-image.png').convert('RGB')
m=p.convert('L').point(lambda v:255 if v>232 else 0)
for xy in [(0,0),(p.width-1,0),(p.width-1,p.height//2)]:
    if m.getpixel(xy)==255: ImageDraw.floodfill(m,xy,128)
a=m.point(lambda v:0 if v==128 else 255).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
p.putalpha(a)
assert a.getpixel((5,5))==0 and a.getpixel((450,700))==255, 'recorte fallido'
sc=820/p.height; p=p.resize((int(p.width*sc),820),Image.LANCZOS)
# halo amarillo detrás de la persona
glow=Image.new('RGBA',(W,H),(0,0,0,0)); g=p.split()[3].filter(ImageFilter.GaussianBlur(25))
glow.paste(Image.new('RGBA',p.size,GOLD+(200,)),(-30,0),g)
bg=Image.alpha_composite(bg.convert('RGBA'),glow); bg.alpha_composite(p,(-30,0))

# captura del reel con borde, giro y sombra
c=Image.open(U+'e8d656db-image.png').convert('RGB'); c=c.resize((int(c.width*390/c.height),390),Image.LANCZOS)
ImageDraw.Draw(c).ellipse((4,352,100,386),outline=GOLD,width=5)
c=ImageOps.expand(c,8,fill='white').convert('RGBA').rotate(5,expand=True,resample=Image.BICUBIC)
sh=Image.new('RGBA',c.size,(0,0,0,0)); sh.putalpha(c.split()[3].point(lambda v:v*0.7).filter(ImageFilter.GaussianBlur(14)))
cx,cy=975,290; bg.alpha_composite(sh,(cx+12,cy+16)); bg.alpha_composite(c,(cx,cy))

d=ImageDraw.Draw(bg)
# flecha del dedo a la captura
d.line([(520,500),(930,500)],fill=GOLD,width=16); d.polygon([(965,500),(915,466),(915,534)],fill=GOLD)

# texto
def txt(s,xy,size,fill):
    f=ImageFont.truetype(F,size); d.text(xy,s,font=f,fill=fill,stroke_width=max(4,size//22),stroke_fill='black')
txt('1,3M',(570,0),215,GOLD)
txt('EN 3 SEMANAS',(570,228),86,'white')
bg.convert('RGB').save(S+'/miniatura_v2.png')
