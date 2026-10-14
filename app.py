import html
import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Studio", page_icon="✨", layout="wide")

st.title("✨ Hello World Studio")
st.write("Create a personalized greeting, choose its style, and add a looping animated effect.")

# Controls
with st.sidebar:
    st.header("Customize your greeting")
    name = st.text_input("Your name", value="World", max_chars=60)
    font = st.selectbox(
        "Font style",
        [
            "Arial", "Georgia", "Verdana", "Trebuchet MS", "Courier New",
            "Impact", "Times New Roman", "Comic Sans MS", "monospace", "serif",
        ],
    )
    font_size = st.slider("Font size", min_value=24, max_value=100, value=56, step=2)
    background = st.selectbox(
        "Background",
        [
            "Sunset", "Ocean", "Forest", "Lavender", "Midnight", "Candy", "Paper",
        ],
    )
    effect = st.selectbox(
        "Animated effect",
        ["None", "Rain", "Snow", "Hail", "Wind gusts", "Confetti", "Tornadoes"],
    )
    text_color = st.selectbox("Text color", ["White", "Black", "Gold", "Coral", "Cyan"])
    bold = st.checkbox("Bold text", value=True)
    italic = st.checkbox("Italic text", value=False)

backgrounds = {
    "Sunset": ("#ff9966", "#ff5e62", "#5b247a"),
    "Ocean": ("#2193b0", "#6dd5ed", "#0b3954"),
    "Forest": ("#134e5e", "#71b280", "#163a24"),
    "Lavender": ("#c9a7eb", "#f4d9ff", "#6a4c93"),
    "Midnight": ("#090979", "#020024", "#1b1b3a"),
    "Candy": ("#ff9a9e", "#fad0c4", "#a18cd1"),
    "Paper": ("#fdfbfb", "#ebedee", "#d5d9df"),
}
colors = {
    "White": "#ffffff",
    "Black": "#111111",
    "Gold": "#ffd166",
    "Coral": "#ff6b6b",
    "Cyan": "#7df9ff",
}

safe_name = html.escape(name.strip() or "World")
bg1, bg2, bg3 = backgrounds[background]
fg = colors[text_color]
font_css = "'" + font.replace("'", "") + "'"
weight = "700" if bold else "400"
style = "italic" if italic else "normal"

# Add a stable set of particles. CSS animations keep moving without repeated Streamlit reruns.
random.seed(17)
particles = []
particle_count = 72 if effect in ("Rain", "Snow", "Hail", "Confetti") else 36
for i in range(particle_count):
    left = random.randint(0, 100)
    delay = random.uniform(-12, 0)
    duration = random.uniform(2.5, 8.0)
    size = random.randint(4, 12)
    drift = random.randint(-100, 100)
    hue = random.randint(0, 360)
    particles.append(
        f'<span class="particle p{i}" style="--left:{left}%;--delay:{delay:.2f}s;'
        f'--duration:{duration:.2f}s;--size:{size}px;--drift:{drift}px;--hue:{hue}deg"></span>'
    )

effect_class = {
    "None": "none",
    "Rain": "rain",
    "Snow": "snow",
    "Hail": "hail",
    "Wind gusts": "wind",
    "Confetti": "confetti",
    "Tornadoes": "tornado",
}[effect]

# Effect-specific particle shapes and motion are all CSS-based, so they loop continuously.
html_doc = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: transparent; font-family: Arial, sans-serif; }}
.scene {{
  position: relative; height: 440px; width: 100%; overflow: hidden; border-radius: 22px;
  background: linear-gradient(135deg, {bg1}, {bg2} 55%, {bg3});
  display: flex; align-items: center; justify-content: center; isolation: isolate;
  box-shadow: 0 12px 32px rgba(0,0,0,.18);
}}
.scene::before {{
  content: ""; position: absolute; inset: -35%;
  background: radial-gradient(circle at 20% 25%, rgba(255,255,255,.28), transparent 28%),
              radial-gradient(circle at 80% 75%, rgba(255,255,255,.16), transparent 30%);
  animation: glow 9s ease-in-out infinite alternate; z-index: -1;
}}
.greeting {{
  position: relative; z-index: 2; max-width: 90%; overflow-wrap: anywhere; text-align: center;
  font-family: {font_css}; font-size: {font_size}px; font-weight: {weight}; font-style: {style};
  color: {fg}; line-height: 1.15; padding: 24px;
  text-shadow: 0 3px 14px rgba(0,0,0,.22);
  animation: greet 3s ease-in-out infinite;
}}
.particle {{ position: absolute; top: -14%; left: var(--left); animation-delay: var(--delay);
  animation-duration: var(--duration); animation-iteration-count: infinite; animation-timing-function: linear; }}
.rain .particle {{ width: 2px; height: 18px; background: rgba(220,245,255,.8); animation-name: rain; }}
.snow .particle {{ width: var(--size); height: var(--size); border-radius: 50%; background: white;
  box-shadow: 0 0 7px rgba(255,255,255,.7); animation-name: snow; }}
.hail .particle {{ width: calc(var(--size) * .8); height: calc(var(--size) * .8); border-radius: 50%;
  background: #eaf8ff; box-shadow: 0 0 4px #fff; animation-name: hail; }}
.confetti .particle {{ width: calc(var(--size) * .8); height: calc(var(--size) * 1.7);
  background: hsl(var(--hue), 90%, 65%); animation-name: confetti; }}
.wind .particle {{ top: auto; left: -35%; width: 24%; height: 2px; border-radius: 99px;
  background: rgba(255,255,255,.6); animation-name: wind; }}
.tornado .particle {{ top: 48%; left: 50%; width: calc(var(--size) * 1.3); height: 3px;
  border-radius: 50%; background: rgba(255,255,255,.7); animation-name: swirl; }}
.none .particle {{ display: none; }}
@keyframes rain {{ from {{ transform: translate3d(0,-10px,0); }} to {{ transform: translate3d(var(--drift),520px,0); }} }}
@keyframes snow {{ 0% {{ transform: translate3d(0,-20px,0) rotate(0); }} 100% {{ transform: translate3d(var(--drift),520px,0) rotate(360deg); }} }}
@keyframes hail {{ 0% {{ transform: translate3d(0,-20px,0); }} 100% {{ transform: translate3d(calc(var(--drift) * .35),520px,0); }} }}
@keyframes confetti {{ 0% {{ transform: translate3d(0,-20px,0) rotate(0); }} 100% {{ transform: translate3d(var(--drift),520px,0) rotate(900deg); }} }}
@keyframes wind {{ 0% {{ transform: translateX(0) scaleX(.5); opacity: 0; }} 20% {{ opacity: .8; }}
  100% {{ transform: translateX(650px) scaleX(1.4); opacity: 0; }} }}
@keyframes swirl {{ 0% {{ transform: rotate(0deg) translateX(15px) scaleX(1.2); opacity: .1; }}
  50% {{ opacity: .9; }} 100% {{ transform: rotate(720deg) translateX(150px) scaleX(.5); opacity: 0; }} }}
@keyframes glow {{ from {{ transform: rotate(0deg) scale(1); }} to {{ transform: rotate(12deg) scale(1.12); }} }}
@keyframes greet {{ 0%,100% {{ transform: translateY(0) scale(1); }} 50% {{ transform: translateY(-5px) scale(1.015); }} }}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; }}
}}
</style>
</head>
<body>
  <div class="scene">
    <div class="particles {effect_class}">{''.join(particles)}</div>
    <div class="greeting">Hello, {safe_name}!</div>
  </div>
</body>
</html>
"""

# Keep the animation inside an iframe so its CSS can run continuously without rerunning the app.
components.html(html_doc, height=460, scrolling=False)

st.caption(
    "Tip: change the options in the sidebar to experiment. The animation runs in a continuous CSS loop; "
    "choose “None” to turn it off."
)
