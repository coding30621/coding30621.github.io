from flask import Flask, request, render_template

app = Flask(__name__)

data_=[]
@app.route("/")
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

@app.route("/<date>", methods=['GET', 'POST'])
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
