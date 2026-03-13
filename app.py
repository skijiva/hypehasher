import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

def hype_hash(input_string):
    if not input_string:
        raise ValueError("empty string")
    
    dick = 't54iLckQl21IYmxbqKoXsfuC0nepazR6BVDEHTOSAjNwW7yPMg9vJ83GrFUdZh'
    
    massiv = [(ord(char) * (i + 1)) % 256 for i, char in enumerate(input_string)]
    
    for _ in range(4):
        for i in range(len(massiv)):
            massiv[i] = (massiv[i] ^ massiv[i - 1] ^ (i * 31)) % 256

    state = 0
    for i, v in enumerate(massiv):
        state = (state * 1000003 ^ v * (i + 1)) & 0xFFFFFFFF  

    result = []
    for i in range(31):
        idx = (massiv[i % len(massiv)] ^ (state >> (i % 32)) ^ i * 10007) % len(dick)
        result.append(dick[idx])
        state = (state * 6364136223846793005 + 1) & 0xFFFFFFFF  

    return "".join(result)

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HYPE HASHER</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0a0a0a;
    --fg: #f0f0f0;
    --dim: #444;
    --border: #2a2a2a;
  }

  html, body {
    height: 100%;
    background: var(--bg);
    color: var(--fg);
    font-family: 'Space Mono', monospace;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
    width: min(620px, 90vw);
    padding: 0 0 4rem;
  }

  .title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 10vw, 6rem);
    letter-spacing: 0.05em;
    line-height: 1;
    color: var(--fg);
    position: relative;
  }

  .title::after {
    content: '';
    display: block;
    height: 1px;
    background: var(--border);
    margin-top: 1.4rem;
    margin-bottom: 2.4rem;
  }

  .subtitle {
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--dim);
    position: absolute;
    top: 0.35em;
    right: 0;
    font-family: 'Space Mono', monospace;
  }

  label {
    display: block;
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--dim);
    margin-bottom: 0.75rem;
  }

  .input-wrap { position: relative; }

  input[type="text"] {
    width: 100%;
    background: transparent;
    border: none;
    border-bottom: 1px solid var(--border);
    color: var(--fg);
    font-family: 'Space Mono', monospace;
    font-size: 1.15rem;
    padding: 0.5rem 0;
    outline: none;
    transition: border-color 0.2s;
    caret-color: var(--fg);
  }

  input[type="text"]::placeholder { color: var(--dim); }
  input[type="text"]:focus { border-bottom-color: var(--fg); }

  .cursor-line {
    position: absolute;
    bottom: 0; left: 0;
    height: 1px; width: 0;
    background: var(--fg);
    transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  }

  input[type="text"]:focus ~ .cursor-line { width: 100%; }

  .char-count {
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    color: var(--dim);
    text-align: right;
    margin-top: 0.5rem;
  }

  .divider {
    height: 1px;
    background: var(--border);
    margin: 2.5rem 0;
  }

  .output-label {
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--dim);
    margin-bottom: 0.75rem;
  }

  .hash-value {
    font-size: 1.05rem;
    letter-spacing: 0.08em;
    color: var(--fg);
    min-height: 1.6em;
    word-break: break-all;
    transition: opacity 0.15s;
    position: relative;
    padding-left: 1.8rem;
  }

  .hash-value::before {
    content: '→';
    position: absolute;
    left: 0;
    color: var(--dim);
    font-size: 0.85rem;
    top: 0.05em;
  }

  .hash-value.loading { opacity: 0.3; }

  .empty-state { color: var(--dim); font-size: 0.85rem; }
</style>
</head>
<body>
<div class="container">
  <div class="title" style="position:relative;">
    HYPE HASHER
    <span class="subtitle">v1.0</span>
  </div>

  <div>
    <label for="inp">Hash your string</label>
    <div class="input-wrap">
      <input type="text" id="inp" placeholder="type something..." autocomplete="off" spellcheck="false">
      <div class="cursor-line"></div>
    </div>
    <div class="char-count"><span id="count">0</span> symblos</div>
  </div>

  <div class="divider"></div>

  <div>
    <div class="output-label">hash</div>
    <div class="hash-value" id="output">
      <span class="empty-state">— awaiting</span>
    </div>
  </div>
</div>

<script>
  const inp = document.getElementById('inp');
  const output = document.getElementById('output');
  const count = document.getElementById('count');
  let debounce;

  inp.addEventListener('input', () => {
    const val = inp.value;
    count.textContent = val.length;
    clearTimeout(debounce);
    output.classList.add('loading');
    debounce = setTimeout(() => computeHash(val), 80);
  });

  async function computeHash(val) {
    try {
      const res = await fetch('/hash', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: val })
      });
      const data = await res.json();
      output.textContent = data.result;
      output.classList.remove('loading');
    } catch {
      output.textContent = 'error';
      output.classList.remove('loading');
    }
  }
</script>
</body>
</html>"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/hash', methods=['POST'])
def hash_route():
    data = request.get_json()
    text = data.get('input', '')
    if not text:
        return jsonify({'result': ''})
    return jsonify({'result': hype_hash(text)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 1337)))
