import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)


def hype_hash(input_string):
    if not input_string:
        return ""

    massiv = []
    result = []
    chet = 0
    nechet = 0
    dick = 't54iLckQl21IYmxbqKoXsfuC0nepazR6BVDEHTOSAjNwW7yPMg9vJ83GrFUdZh'

    for char in input_string:
        temp = ord(char) % len(input_string)
        massiv.append(temp)

    for i in range(len(massiv) - 1):
        if i % 2 == 0:
            chet += massiv[i]
        else:
            nechet += massiv[i]

    temp = nechet + 1
    nechet = nechet % (chet + 1)
    chet = chet % temp
    value = chet + nechet

    for i in range(31):
        idx = (massiv[i % (len(input_string))] + value + i * 10007) % len(dick)
        result.append(dick[idx])

    return "".join(result)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HYPE HASHER</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #121212;
            color: #ffffff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            width: 100%;
            max-width: 600px;
            padding: 20px;
            text-align: center;
        }
        h1 {
            font-weight: normal;
            letter-spacing: 4px;
            margin-bottom: 40px;
            text-transform: uppercase;
            border-bottom: 2px solid #ffffff;
            padding-bottom: 10px;
            display: inline-block;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            font-size: 18px;
            background-color: #000000;
            color: #ffffff;
            border: 2px solid #555555;
            outline: none;
            box-sizing: border-box;
            transition: border-color 0.3s ease;
            text-align: center;
        }
        input[type="text"]:focus {
            border-color: #ffffff;
        }
        .result-box {
            margin-top: 30px;
            min-height: 25px;
            padding: 20px;
            border: 1px dashed #555555;
            font-size: 24px;
            word-wrap: break-word;
            letter-spacing: 2px;
            color: #ffffff;
        }
        .placeholder {
            color: #555555;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hype Hasher</h1>

        <input type="text" id="userInput" placeholder="Введите строку..." autocomplete="off">

        <div class="result-box" id="hashResult">
            <span class="placeholder">Результат появится здесь...</span>
        </div>
    </div>

    <script>
        const inputField = document.getElementById('userInput');
        const resultBox = document.getElementById('hashResult');

        inputField.addEventListener('input', async function() {
            const text = this.value;

            if (text.length === 0) {
                resultBox.innerHTML = '<span class="placeholder">Результат появится здесь...</span>';
                return;
            }

            try {
                const response = await fetch('/api/hash', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: text })
                });

                if (response.ok) {
                    const data = await response.json();
                    resultBox.textContent = data.hash; 
                } else {
                    resultBox.textContent = 'Ошибка вычисления';
                }
            } catch (error) {
                resultBox.textContent = 'Ошибка соединения с сервером';
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/hash', methods=['POST'])
def api_hash():
    data = request.get_json()
    text = data.get('text', '')

    hashed_result = hype_hash(text)

    return jsonify({'hash': hashed_result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 1337))
    app.run(host='0.0.0.0', port=port)
