from flask import Flask, request, render_template

app = Flask(__name__)

yet = []
fin = []

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        yet.append(request.form['input'])
    return '''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3-6 온라인 소리함</title>
</head>
<body>
<form action="/" method="POST">
    <p><textarea rows="4" cols="50" name="input" placeholder="입력란"></textarea></p>
    <p><input type="submit" value="확인"></p>
</form>
</body>
</html>
'''

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['remove'] != "":
            remove = int(request.form['remove']) - 1
            del yet[remove]
        if request.form['solve'] != "":
            solve = int(request.form['solve']) - 1
            fin.append(yet[solve])
            del yet[solve]
        if request.form['unsolve'] != "":
            unsolve = int(request.form['unsolve']) - 1
            yet.append(fin[unsolve])
            del fin[unsolve]
    output = ''
    num = 0
    output = output + '해결 필요'
    for topic in yet:
        num += 1
        output = output + f'<p>{num}. {topic}</p>'
    output = output + '<br><br>'
    output = output + '해결 완료'
    num = 0
    for topic in fin:
        num += 1
        output = output + f'<p>{num}. {topic}</p>'
    return f'''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>admin</title>
</head>
<body>
{output}
<form action="/admin" method="POST">
    <p><input name="remove" type="text" placeholder="제거" value=""></p>
    <p><input name="solve" type="text" placeholder="해결" value=""></p>
    <p><input name="unsolve" type="text" placeholder="미해결" value=""></p>
    <p><input type="submit" value="확인"></p>
</form>
</body>
</html>
'''


app.run(debug=True)
