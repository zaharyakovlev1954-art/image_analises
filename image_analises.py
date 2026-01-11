from flask import Flask, request, render_template_string
import io

app = Flask(__name__)

# HTML форма с правильными кавычками
HTML_FORM = '''
<!DOCTYPE html>
<html>
<body>
    <h2>StegoWatch - LSB анализатор</h2>
    <form action="/analyze" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".bmp,.png,.jpg">
        <button type="submit">Анализировать файл</button>
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return 'Ошибка: файл не загружен'
    
    file = request.files['file']
    if file.filename == '':
        return 'Ошибка: не выбран файл'
    
    # Анализ LSB
    try:
        file_bytes = file.read()
        if len(file_bytes) < 100:
            return 'Ошибка: файл слишком маленький (меньше 100 байт)'
        
        number_bytes = 0
        number_bits_1 = 0
        
        for byte in file_bytes:
            number_bytes += 1  # один байт = 8 бит, но мы считаем байты
            if byte & 1 == 1:  # проверяем младший бит
                number_bits_1 += 1
        
        ratio = number_bits_1 / number_bytes
        
        if 0.48 <= ratio <= 0.52:
            return f'<h2 style="color: green;">✅ Файл безопасен</h2>'"\n⚠️ Внимание: анализ проведён по всем байтам файла, включая заголовки. Для точного результата используйте BMP 24-bit."
        else:
            return f'<h2 style="color: red;">⚠️ Подозрительный файлZ</h2>'"\n⚠️ Внимание: анализ проведён по всем байтам файла, включая заголовки. Для точного результата используйте BMP 24-bit."
    
    except Exception as e:
        return f'Ошибка при анализе: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
