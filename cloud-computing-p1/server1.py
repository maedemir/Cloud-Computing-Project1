from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import database as d
import rabbitmq as r
import image_storage as i
from PIL import Image
import base64
import io

import mail as m

app = Flask(__name__,static_folder='../Flask', template_folder='../Flask')
UPLOAD_FOLDER = './temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def root():
   return render_template('./front/index.html')

@app.route('/index.html')
def index():
   return render_template('./front/index.html')

@app.route('/uploader', methods = ['POST'])
def uploader():
   if request.method == "POST":
      file = request.files['picture']
      text = request.form['text']
      email = request.form['email']
      if file:
         print(email)
         print(text)
         print(file)

         d.database_insert(cursor,connection,text,email,"in progress"," not identified")
         count = d.database_show_all(cursor)
         name = str(count) + ".png"
         print("file uploaded")
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
         path = os.path.join(app.config['UPLOAD_FOLDER'], name)
         i.upload_image_s3(path,name)
         os.remove(path)
         print("file removed")
         r.RabbitMQ_send(count)
         data = [
            {
               'id': count
            }
         ]
         
      return render_template('./front/add_response.html' , data=data)

@app.route('/downloader', methods = ['POST'])
def downloader():
   cursor,connection = d.database_connection()
   d.database_show_all(cursor)
   if request.method == "POST":
      id = request.form['id']
      print(id)
      empty,result = d.database_get_data(cursor,id)
      if empty == 1:
         data = [
            {
               'state': "ID is invalid"
            }
         ]
         return render_template('./front/ad_detail_reject.html' , data=data) 
      else: 
         print(result)
         if result['state'] == "in progress":
            data = [
               {
                  'state': "Your ad has not been reviewed yet"
               }
            ]
            return render_template('./front/ad_detail_reject.html' , data=data)
         elif result['state'] == "rejected":
            data = [
               {
                  'state': "Your ad has not been accepted"
               }
            ]
            return render_template('./front/ad_detail_reject.html' , data=data)
         elif result['state'] == "accepted":
            i.download_image_s3(id)
            name = "./temp/"+str(id)+".png"
            im = Image.open(name)
            data_image = io.BytesIO()
            im.save(data_image, "PNG")
            encoded_img_data = base64.b64encode(data_image.getvalue())
            data = [
               {
                  'state': "Your ad has been accepted",
                  'address': encoded_img_data.decode('utf-8'),
                  'text': result['description'],
                  'category': result['category']
               }
            ]
            os.remove(name)
            return render_template('./front/ad_detail.html' , data=data , file= '../download/'+str(id)+'.png')

def fix_connection():
   connection.commit()
   d.database_show_all()

if __name__ == '__main__':
   cursor,connection = d.database_setup(1) # 0: we don't have database    1: we have database(drop first)
   app.secret_key = ".."
   app.run(debug=False)