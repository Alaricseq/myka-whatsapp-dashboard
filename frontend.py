from flask import Flask, render_template, request, redirect, url_for
from backend import contacts_collection, logs_collection, twilio_client, twilio_whatsapp_number

app = Flask(__name__)

@app.route('/')
def index():
    contacts = list(contacts_collection.find({}, {"_id": 0}))
    return render_template("index.html", contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        contacts_collection.insert_one({'name': name, 'number': number})
        return redirect(url_for('index'))
    return render_template("add_contact.html")

@app.route('/send_message', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        number = request.form['number']
        body = request.form['body']
        image_url = request.form['image_url']
        # Send WhatsApp message with optional image
        message = twilio_client.messages.create(
            body=body + " (Sent from Twilio trial account)",
            from_=twilio_whatsapp_number,
            to="whatsapp:" + number,
            media_url=[image_url] if image_url else None
        )
        logs_collection.insert_one({
            "to": number,
            "body": body,
            "image": image_url,
            "status": "sent",
            "sid": message.sid
        })
        return redirect(url_for('logs'))
    contacts = list(contacts_collection.find({}, {"_id": 0}))
    return render_template("send_message.html", contacts=contacts)


@app.route('/logs')
def logs():
    logs = list(logs_collection.find({}, {"_id": 0}))
    return render_template("logs.html", logs=logs)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
