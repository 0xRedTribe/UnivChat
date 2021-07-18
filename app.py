from flask import Flask, render_template, request
from flask_socketio import SocketIO,emit, join_room, leave_room,send
import os

app = Flask(__name__,template_folder="templates")
app.config['SECRET_KEY'] = os.environ.get('SECRET')
socketio = SocketIO(app)

#Find number of clients
clients = 0         


#---App Routes---

@app.route('/')
def home_html():
    return render_template('index.html')


@app.route('/rooms')
def room_html():
    return render_template("rooms.html")

@app.route('/about')
def about():
    return render_template('about.html')

    
#---SUBDIRS /rooms-----
@app.route('/rooms/photography',methods=['GET', 'POST'])
def photoRoom():
    return render_template('photography.html')

@app.route('/rooms/coding',methods=['GET', 'POST'])
def codingRoom():
    return render_template('coding.html')

@app.route('/rooms/memes',methods=['GET', 'POST'])
def memes():
    return render_template('memes.html')

@app.route('/rooms/nerds',methods=['GET', 'POST'])
def nerdsRoom():
    return render_template('nerds.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')



# ---Main Event for HOME(Public) room!----

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    #print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

#--- ROOMS EVENTS----

#ROOM:photography
@socketio.on('ph event',namespace="/rooms/photography")
def handle_my_custom_event(json, methods=['GET', 'POST']):
    #print('received my event: ' + str(json))
    socketio.emit('ph response', json, callback=messageReceived, namespace='/rooms/photography')

#ROOM:coding
@socketio.on('cod event',namespace="/rooms/coding")
def handle_my_custom_event(json,methods=['GET','POST']):
    socketio.emit('cod response',json, callback=messageReceived ,namespace='/rooms/coding')

#ROOM:memes
@socketio.on('meme event',namespace="/rooms/memes")
def handle_my_custom_event(json,methods=['GET','POST']):
    socketio.emit('meme response',json, callback=messageReceived ,namespace='/rooms/memes')

#ROOM:nerds
@socketio.on('nerd event',namespace="/rooms/nerds")
def handle_my_custom_event(json,methods=['GET','POST']):
    socketio.emit('nerd response',json, callback=messageReceived ,namespace='/rooms/nerds')


#----Client Counting(public)-----
@socketio.on("connect")
def count_connection():
    print("\n",request.sid + " Connected Successfully. [ 2 0 0 ]")
    global clients
    clients += 1
    emit("users",{"count":clients},broadcast=True)

@socketio.on("disconnect")
def count_disconn():
    global clients
    clients = clients - 1
    emit("users",{"count":clients},broadcast=True)




if  __name__ == '__main__':
    app.run()