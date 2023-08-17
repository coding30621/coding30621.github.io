from flask import Flask, request, render_template

app = Flask(__name__)

yet = []
fin = []

@app.route("/", methods=['GET', 'POST'])
def index_():
    if request.method == 'POST':
        yet.append(request.form['input'])
    return render_template('index_.html')

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

data_=[]
@app.route("/timetable")
def index():
    data = 'var events = ['
    year_added = []
    month_added = []
    day_added = []
    overlap = []
    for i in data_:
        if i[2] in day_added:
            if i[1] in month_added:
                if i[0] in year_added:
                    overlap.append([i[0],i[1],i[2]])
        else:
            day_added.append(i[2])
            month_added.append(i[1])
            year_added.append(i[0])
    for i in data_:
        new = '{ date: new Date('+str(i[0])+','+str(i[1]-1)+','+str(i[2])+'),title:"'+i[3]
        for j in overlap:
            if i[0] == j[0]:
                if i[1] == j[1]:
                    if i[2] == j[2]:
                        new = new + "."
        new = new + '"},'
        data = data + new
    data = data + '];'
    return render_template('index.html', data=data)

@app.route("/timetable/<date>", methods=['GET', 'POST'])
def date(date):
    year=int(date[0:4])
    month=int(date[5:7])
    day=int(date[8:10])
    data='var scheduleList = ['
    to_do = []
    for i in data_:
        if i[2] == day:
            if i[1] == month:
                if i[0] == year:
                    to_do.append(i)
    if request.method == 'POST':
        if request.form['time'] != "":
            if request.form['activity'] != "":
                a = [year,month,day,request.form['activity'],request.form['time']]
                if a in to_do:
                    pass
                else:
                    data_.append(a)
                    to_do.append(a)
    for i in to_do:
        new = '{ time: "'+i[4]+'",activity:"'+i[3]
        new = new + '"},'
        data = data + new
    data = data + '];'
    return render_template('date.html', data=data, date=date)

app.run()
