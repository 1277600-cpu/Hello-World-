import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="✨", layout="wide")

st.title("Hello World Motion Lab")
st.caption("A tiny creative coding playground — change the controls and watch your name come to life.")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", value="Hello World", max_chars=80)
    font_family = st.selectbox(
        "Font type",
        ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS", "Impact", "monospace", "sans-serif", "serif"],
    )
    font_size = st.slider("Font size (px)", min_value=20, max_value=100, value=48, step=2)
    background = st.selectbox(
        "Background",
        ["Light", "Dark", "Ocean", "Sunset", "Forest", "Lavender"],
    )
    name_mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox(
        "Dynamic action",
        ["None", "Rain", "Snow", "Hail", "Wind Gust", "Confetti", "Tornado"],
    )
    animation_speed = st.slider("Animation speed", min_value=0.5, max_value=2.5, value=1.0, step=0.1,
                                help="Higher values make the effect move faster.")
    particle_count = st.slider("Effect density", min_value=10, max_value=70, value=35, step=5)

backgrounds = {
    "Light": ("#f8fafc", "#111827"),
    "Dark": ("#080b16", "#f8fafc"),
    "Ocean": ("#06283d", "#e0f7ff"),
    "Sunset": ("#3b164a", "#fff3d6"),
    "Forest": ("#102a1e", "#efffee"),
    "Lavender": ("#eee7ff", "#2d174d"),
}
bg_color, text_color = backgrounds[background]
safe_name = html.escape(name or "Hello World")
safe_font = html.escape(font_family, quote=True)

# Build particles with CSS animations. Animation runs inside the component, so it
# loops continuously without repeatedly rerunning the Streamlit Python script.
rng = random.Random(17)
particles = []
for i in range(particle_count):
    left = rng.randint(0, 100)
    delay = rng.uniform(-12, 0)
    duration = rng.uniform(3.0, 8.0) / animation_speed
    size = rng.randint(12, 25)
    drift = rng.randint(-100, 100)
    if effect == "Rain":
        symbol, klass = "💧", "fall rain"
    elif effect == "Snow":
        symbol, klass = "❄", "fall snow"
    elif effect == "Hail":
        symbol, klass = "🧊", "fall hail"
    elif effect == "Confetti":
        symbol, klass = rng.choice(["🎉", "🟣", "🟡", "🟢", "🔵", "🩷"]), "fall confetti"
    elif effect == "Wind Gust":
        symbol, klass = rng.choice(["〰", "🍃", "➤", "💨"]), "wind"
    elif effect == "Tornado":
        symbol, klass = rng.choice(["·", "○", "◦", "🌀"]), "tornado-particle"
    else:
        continue
    particles.append(
        f'<span class="particle {klass}" style="--left:{left}%;--delay:{delay:.2f}s;'
        f'--duration:{duration:.2f}s;--size:{size}px;--drift:{drift}px;--index:{i};">{symbol}</span>'
    )

particles_html = "".join(particles)
if effect == "None":
    effect_html = ""
elif effect == "Tornado":
    effect_html = f'<div class="tornado-core" aria-hidden="true"></div>{particles_html}'
else:
    effect_html = particles_html

if name_mode == "Ticker Tape":
    display_html = f'<div class="name ticker">{safe_name}<span class="ticker-gap"> ✦ {safe_name}</span></div>'
elif name_mode == "Repeated":
    display_html = '<div class="name repeated">' + "<br>".join([safe_name] * 5) + "</div>"
else:
    display_html = f'<div class="name centered">{safe_name}</div>'

ticker_css = """
.name.ticker { white-space: nowrap; width: max-content; animation: marquee 12s linear infinite; }
.ticker-gap { padding-left: 5rem; }
@keyframes marquee { from { transform: translateX(100%); } to { transform: translateX(-100%); } }
""" if name_mode == "Ticker Tape" else ""

css = f"""
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
.stage {{
  position: relative; height: 650px; width: 100%; overflow: hidden;
  border-radius: 18px; background: {bg_color}; color: {text_color};
  font-family: {safe_font}, sans-serif; isolation: isolate;
}}
.stage::before {{
  content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .24;
  background: radial-gradient(circle at 15% 20%, #8b5cf6 0, transparent 30%),
              radial-gradient(circle at 85% 80%, #06b6d4 0, transparent 32%);
}}
.effects {{ position: absolute; inset: 0; overflow: hidden; pointer-events: none; z-index: 1; }}
.name-layer {{ position: absolute; inset: 0; z-index: 3; display: flex; align-items: center;
  justify-content: center; overflow: hidden; padding: 24px; }}
.name {{ font-size: {font_size}px; font-weight: 700; line-height: 1.25; text-shadow: 0 2px 14px rgba(0,0,0,.18); }}
.name.centered {{ text-align: center; overflow-wrap: anywhere; }}
.name.repeated {{ width: 100%; text-align: center; line-height: 1.45; }}
.particle {{ position: absolute; top: -12%; left: var(--left); font-size: var(--size);
  opacity: .88; user-select: none; will-change: transform; }}
.fall {{ animation: fall var(--duration) linear var(--delay) infinite; }}
.rain {{ filter: saturate(1.25); }}
.snow {{ animation-name: snowfall; }}
.hail {{ animation-name: hailfall; }}
.confetti {{ animation-name: confettifall; }}
@keyframes fall {{ 0% {{ transform: translate3d(0,-10vh,0); }} 100% {{ transform: translate3d(var(--drift),115vh,0); }} }}
@keyframes snowfall {{ 0% {{ transform: translate3d(0,-10vh,0) rotate(0); }} 100% {{ transform: translate3d(calc(var(--drift) * 1.5),115vh,0) rotate(540deg); }} }}
@keyframes hailfall {{ 0% {{ transform: translate3d(0,-10vh,0); }} 100% {{ transform: translate3d(calc(var(--drift) * .25),115vh,0); }} }}
@keyframes confettifall {{ 0% {{ transform: translate3d(0,-10vh,0) rotate(0); }} 100% {{ transform: translate3d(var(--drift),115vh,0) rotate(900deg); }} }}
.wind {{ top: var(--left); left: -20%; animation: gust var(--duration) ease-in-out var(--delay) infinite; }}
@keyframes gust {{ 0% {{ transform: translateX(-20vw) rotate(0); opacity: 0; }} 15% {{ opacity: .9; }}
  85% {{ opacity: .8; }} 100% {{ transform: translateX(140vw) rotate(18deg); opacity: 0; }} }}
.tornado-core {{ position:absolute; z-index:2; left:50%; top:50%; width: min(42vw,360px); height: 80%;
  transform: translate(-50%,-50%); border-radius: 50%;
  background: repeating-conic-gradient(from 0deg, rgba(160,190,210,.05) 0deg 12deg, rgba(160,190,210,.35) 14deg 20deg, transparent 22deg 34deg);
  filter: blur(2px); animation: spin 2.8s linear infinite; mask-image: linear-gradient(to bottom, transparent, black 15%, black 75%, transparent); }}
.tornado-particle {{ top: calc(15% + (var(--index) * 1%)); left: 50%;
  animation: swirl calc(2.6s / {animation_speed}) linear var(--delay) infinite; }}
@keyframes spin {{ to {{ rotate: 360deg; }} }}
@keyframes swirl {{ 0% {{ transform: rotate(0deg) translateX(18px) scale(.5); opacity:.1; }}
  50% {{ opacity:.9; }} 100% {{ transform: rotate(360deg) translateX(180px) scale(1.1); opacity:.1; }} }}
{ticker_css}
@media (prefers-reduced-motion: reduce) {{
  .particle, .name.ticker, .tornado-core {{ animation-duration: 30s !important; }}
}}
</style>
"""

html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8">{css}</head>
<body>
<div class="stage">
  <div class="effects" aria-hidden="true">{effect_html}</div>
  <div class="name-layer">{display_html}</div>
</div>
</body></html>"""

components.html(html_doc, height=670, scrolling=False)
st.caption("Tip: choose an effect, then change its density or speed. The animation loops inside the preview.")
