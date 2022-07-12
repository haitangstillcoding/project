import os

from flask import Flask, render_template, jsonify
from flask_apscheduler import APScheduler

import utils

app = Flask(__name__)

u = utils.utils("epidemic", "root", "root")


def crawl_data():
    cur_path = os.path.dirname(os.path.abspath(__file__))
    os.system("python {}".format(os.path.join(cur_path, "spider.py")))


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/c1')
def get_c1_data():
    data = u.get_c1_data()
    print(data)
    return jsonify({"confirm": data[0], "heal": data[1], "dead": data[2], "nowConfirm": data[3]})


@app.route('/c2')
def get_c2_data():
    res = []
    data = u.get_c2_data()
    for key, value in data.items():
        res.append({"name": key, "value": value})
    return jsonify({"data": res})


@app.route('/l1')
def get_l1_data():
    data = u.get_l1_data()
    day = data.date.tolist()
    importedCase = data.importedCase.tolist()
    noInfect = data.noInfect.tolist()
    dead = data.dead.tolist()
    return jsonify({"days": day, "importedCase": importedCase, "noInfect": noInfect, "dead": dead})


@app.route('/l2')
def get_l2_data():
    data = u.get_l2_data()
    day = data.date.tolist()
    localConfirmadd = data.localConfirmadd.tolist()
    heal = data.heal.tolist()
    dead = data.dead.tolist()
    return jsonify({"days": day, "localConfirmadd": localConfirmadd, "heal": heal, "dead": dead})


@app.route('/r1')
def get_r1_data():
    data = u.get_r1_data()
    keys = data.province.tolist()
    values = data.zero.tolist()
    return jsonify({"keys": keys, "values": values})


@app.route('/r2')
def get_r2_data():
    data = u.get_r2_data()
    day = data.date.tolist()
    heal = data.heal.tolist()
    nowConfirm = data.nowConfirm.tolist()
    confirm = data.confirm.tolist()
    return jsonify({"days": day, "heal": heal, "nowConfirm": nowConfirm, "confir": confirm})


if __name__ == '__main__':
    # Advanced Python Scheduler
    scheduler = APScheduler()
    # 当你想以固定的时间间隔运行任务时使用
    scheduler.add_job(crawl_data, 'interval', days=1)
    scheduler.init_app(app=app)
    # 启动调度程序
    scheduler.start()
    app.run()
