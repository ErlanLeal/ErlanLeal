"""Gera os SVGs do perfil (hero, tagline, títulos e rodapé) a partir de img/top-01.png.
Uso: python tools/build_assets.py  (requer Pillow)
"""
import base64, io
from PIL import Image, ImageDraw, ImageFilter
import pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
D=str(ROOT/'img')+'/'
FONTS=ROOT/'tools'/'fonts'
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
MONO=b64(FONTS/'share-tech-mono-latin-400-normal.woff')
ORB=b64(FONTS/'orbitron-latin-500-normal.woff')
RM="@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
FF=lambda orb=False:(f"@font-face{{font-family:Orb;src:url(data:font/woff;base64,{ORB}) format('woff')}}" if orb else "")+f"@font-face{{font-family:Mono;src:url(data:font/woff;base64,{MONO}) format('woff')}}"


def rule(cx,y,half,uid):
    return f'''<defs><linearGradient id="rg{uid}" x1="0" x2="1"><stop offset="0" stop-color="#ff3b30" stop-opacity="0"/><stop offset=".25" stop-color="#ff3b30"/><stop offset=".5" stop-color="#3a3a3a"/><stop offset=".75" stop-color="#2ee88a"/><stop offset="1" stop-color="#2ee88a" stop-opacity="0"/></linearGradient>
<filter id="rf{uid}" x="-10%" y="-300%" width="120%" height="700%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect class="rl" x="{cx-half}" y="{y-1}" width="{2*half}" height="2" fill="url(#rg{uid})" filter="url(#rf{uid})"/>
<rect class="dia" x="{cx-5}" y="{y-5}" width="10" height="10" fill="#0d1117" stroke="#2ee88a" stroke-width="1.6"/>'''
RULECSS=".rl{animation:pulse 4s ease-in-out infinite}@keyframes pulse{0%,100%{opacity:.65}50%{opacity:1}}.dia{transform-box:fill-box;transform-origin:center;transform:rotate(45deg)}"

# --- banner base: vignette + scanlines only
im=Image.open(D+'top-01.png').convert('RGBA'); W,H=im.size; s=W/2000; P=lambda v:int(v*s)
vg=Image.new('L',(W,H),0); d=ImageDraw.Draw(vg)
for i in range(60):
    d.rectangle([P(i*2),P(i*2),W-P(i*2),H-P(i*2)],outline=int(110*(1-i/60)**2),width=P(2))
blk=Image.new('RGBA',(W,H),(0,0,0,255)); blk.putalpha(vg.filter(ImageFilter.GaussianBlur(P(10))))
im=Image.alpha_composite(im,blk)
sl=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sl)
for y in range(0,H,P(3)): sd.line([(0,y),(W,y)],fill=(0,0,0,22),width=max(1,P(1)))
im=Image.alpha_composite(im,sl).convert('RGB').resize((2400,600),Image.LANCZOS)
buf=io.BytesIO(); im.save(buf,'JPEG',quality=86,optimize=True,progressive=True); IMG=base64.b64encode(buf.getvalue()).decode()

def br(x0,y0,x1,y1,L):
    p=[]
    for x,y,dx,dy in [(x0,y0,1,1),(x1,y0,-1,1),(x0,y1,1,-1),(x1,y1,-1,-1)]:
        p.append(f'M{x+dx*L},{y} L{x},{y} L{x},{y+dy*L}')
    return ' '.join(p)
ticks=''.join(f'<line x1="{1290+i*9}" y1="292" x2="{1290+i*9}" y2="{292+(7 if i%4==0 else 4)}"/>' for i in range(13))
T=9
def corner(x,y,dx,dy,L,ox,oy,cls):
    return f'<g class="c {cls}" style="--ox:{ox}px;--oy:{oy}px"><path d="M{x+dx*L},{y} L{x},{y} L{x},{y+dy*L}"/></g>'
x0,y0,x1,y1,L=930,110,1410,280,24
corners=''.join([corner(x0,y0,1,1,L,-170,-70,'tl'),corner(x1,y0,-1,1,L,170,-70,'tr'),corner(x0,y1,1,-1,L,-170,70,'bl'),corner(x1,y1,-1,-1,L,170,70,'br')])
ticks=''.join(f'<line x1="{1290+i*9}" y1="292" x2="{1290+i*9}" y2="{292+(7 if i%4==0 else 4)}"/>' for i in range(13))
banner=f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="2000" height="500" viewBox="0 0 2000 500">
<style>{FF()}
.all{{animation:life {T}s infinite}}
@keyframes life{{0%{{opacity:0}}3%{{opacity:1}}90%{{opacity:1}}96%,100%{{opacity:0}}}}
.drift{{animation:drift {T}s cubic-bezier(.3,.1,.2,1) infinite}}
@keyframes drift{{0%{{transform:translate(-260px,40px)}}10%{{transform:translate(-90px,-25px)}}17%{{transform:translate(70px,15px)}}24%,100%{{transform:translate(0,0)}}}}
.c path{{fill:none;stroke-width:2;animation:col {T}s steps(1) infinite}}
@keyframes col{{0%{{stroke:#ebebeb}}25%,100%{{stroke:#2ee88a}}}}
.c{{animation:conv {T}s cubic-bezier(.5,0,.2,1) infinite}}
@keyframes conv{{0%{{transform:translate(var(--ox),var(--oy))}}12%{{transform:translate(calc(var(--ox)*.5),calc(var(--oy)*.5))}}24%,100%{{transform:translate(0,0)}}}}
.lockfx{{animation:flash {T}s infinite}}
@keyframes flash{{0%,24%{{opacity:1}}26%{{opacity:.15}}28%{{opacity:1}}30%{{opacity:.15}}32%,100%{{opacity:1}}}}
.cross{{opacity:0;animation:cross {T}s infinite}}
@keyframes cross{{0%,24%{{opacity:0}}25%,100%{{opacity:1}}}}
.scn{{font-family:Mono,monospace;font-size:13px;letter-spacing:2px;fill:#ebebeb;animation:scn {T}s infinite}}
@keyframes scn{{0%,24%{{opacity:.9}}25%,100%{{opacity:0}}}}
.lck{{font-family:Mono,monospace;font-size:13px;letter-spacing:2px;fill:#2ee88a;opacity:0;animation:cross {T}s infinite}}
.lead{{fill:none;stroke:#2ee88a;stroke-width:1.6;stroke-dasharray:340;stroke-dashoffset:340;animation:lead {T}s ease-out infinite}}
@keyframes lead{{0%,32%{{stroke-dashoffset:340}}38%,100%{{stroke-dashoffset:0}}}}
.tag{{font-family:Mono,monospace;font-size:17px;letter-spacing:2px;fill:#2ee88a;opacity:0;animation:tag {T}s infinite}}
@keyframes tag{{0%,38%{{opacity:0}}39%{{opacity:1}}40%{{opacity:.2}}41%,100%{{opacity:1}}}}
.ruler{{opacity:0;animation:cross {T}s infinite}}
.cur{{animation:sweep 3.5s ease-in-out infinite alternate}}
@keyframes sweep{{from{{transform:translateX(0)}}to{{transform:translateX(100px)}}}}
{RM}</style>
<defs>
<filter id="gl" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<image width="2000" height="500" href="data:image/jpeg;base64,{IMG}" xlink:href="data:image/jpeg;base64,{IMG}"/>
<path d="M54,20 L20,20 L20,54 M1946,20 L1980,20 L1980,54 M54,480 L20,480 L20,446 M1946,480 L1980,480 L1980,446" fill="none" stroke="#ebebeb" stroke-opacity=".45" stroke-width="1.8"/>
<g class="all" filter="url(#gl)">
  <g class="drift">
    <g class="lockfx">{corners}</g>
    <text class="scn" x="{x0+4}" y="{y1+20}">SCANNING...</text>
  </g>
  <g class="cross" stroke="#2ee88a" stroke-width="1.6"><line x1="1156" y1="195" x2="1164" y2="195"/><line x1="1176" y1="195" x2="1184" y2="195"/><line x1="1170" y1="181" x2="1170" y2="189"/><line x1="1170" y1="201" x2="1170" y2="209"/></g>
  <text class="lck" x="{x0+4}" y="{y1+20}">LOCKED</text>
  <g class="ruler"><g stroke="#2ee88a" stroke-opacity=".7" stroke-width="1.2">{ticks}</g><rect class="cur" x="1288" y="300" width="6" height="3" fill="#2ee88a"/></g>
  <path class="lead" d="M{x1},{y0} L1490,62 L1730,62"/>
  <text class="tag" x="1500" y="50">TARGET LOCK // AI ENGINEERING</text>
</g>
</svg>'''
open(D+'hero.svg','w').write(banner)

# --- nameplate
name=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="70" viewBox="0 0 900 70">
<style>{FF()}
.r{{font-family:Mono,monospace;font-size:15px;letter-spacing:6px;fill:#8b949e;animation:fade 1.2s .4s ease-out both}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
{RULECSS}
{RM}</style>
{rule(450,18,450,"n")}
<text class="r" x="450" y="52" text-anchor="middle">PLATFORM · DATA · AI</text>
</svg>'''
open(D+'tagline.svg','w').write(name)

# --- section headers
for n,t in [("01","PROFILE"),("02","AI ENGINEERING"),("03","ARSENAL"),("04","MISSIONS"),("05","PILOT")]:
    w=len(t)*14+90; L=900-w
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="76" viewBox="0 0 900 76">
<style>{FF()}
.a{{font-family:Mono,monospace;font-size:20px;letter-spacing:3px}}
{RM}</style>
<g transform="translate(0,36)">
<text class="a" x="0" y="26" fill="#ff3b30">{n}</text>
<text class="a" x="36" y="26" fill="#8b949e">//</text>
<text class="a" x="66" y="26" fill="#c9d1d9">{t}</text>
</g>
</svg>'''
    open(D+f'hdr-{n}.svg','w').write(svg)

# --- footer
foot=f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="110" viewBox="0 0 900 110">
<style>{FF()}
{RULECSS}
.t{{font-family:Mono,monospace;font-size:12px;letter-spacing:4px;fill:#8b949e}}
.m{{font-family:Mono,monospace;font-size:16px;letter-spacing:3px;fill:#2ee88a}}
.k{{font-family:Mono,monospace;font-size:16px;letter-spacing:3px;fill:#ff3b30}}
.cur{{animation:blink 1.2s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
{RM}</style>
{rule(450,20,450,"f")}
<text class="t" x="450" y="60" text-anchor="middle">END OF TRANSMISSION</text>
<text x="450" y="90" text-anchor="middle"><tspan class="k">&gt; </tspan><tspan class="m">ERLAN.RJ@GMAIL.COM</tspan></text>
</svg>'''
open(D+'outro.svg','w').write(foot)
