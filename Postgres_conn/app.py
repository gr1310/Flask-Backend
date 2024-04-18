from flask import Flask, request
import psycopg2

import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO

app= Flask(__name__)
# Function to convert base64 string to numpy array
def base64_to_numpy(base64_string):
    decoded_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(decoded_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np

def rotateImage(images):
    img64= base64_to_numpy(images['ImagePath'])
    # Rotate the image
    rotated_image = cv2.rotate(img64, cv2.ROTATE_90_CLOCKWISE)
    pil_image = Image.fromarray(rotated_image)
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()

    # Encode the bytes using base64
    base64_image = base64.b64encode(image_bytes).decode()
    images['ImagePath']= base64_image
    return images

@app.get("/data/<course_num>")
def home(course_num):
    conn= psycopg2.connect(database="mytestdb",
                       user="postgres",
                       password="123456",
                       host="localhost",
                       port="5432")

    cur = conn.cursor()

    conn.commit()

    cur.execute('''SELECT * FROM public."ImageApp_images" WHERE "ImageId"=%s;'''% course_num)

    data= cur.fetchall()
    # print(data)

    cur.close()
    conn.close()
    return {"image":data[0][1]},200

@app.post("/push")
def add_image():
    image_data= request.get_json()
    # print(image_data)
    image_data= rotateImage(image_data)
    # print(image_data)
    conn= psycopg2.connect(database="mytestdb",
                       user="postgres",
                       password="123456",
                       host="localhost",
                       port="5432")

    cur = conn.cursor()

    final_image=image_data['ImagePath']
    # print(final_image)
    course_num= image_data['ImageId']
    # print("here",course_num)
    cur.execute('''SELECT * FROM public."ImageApp_images" WHERE "ImageId" = %s;''', (course_num,))
    record_exists = cur.fetchone()
    # print(record_exists)
    if record_exists:
        cur.execute('''UPDATE public."ImageApp_images" SET "ImagePath"=%s WHERE "ImageId"=%s;''',(final_image,course_num))
        conn.commit()
    else:
        final_image = image_data['ImagePath']

        cur.execute('''INSERT INTO public."ImageApp_images" ("ImageId", "ImagePath") VALUES (%s, %s);''', (course_num, final_image))
        conn.commit()
    cur.close()
    conn.close()

    return {"message":"added successfully"}, 201

@app.put("/push")
def change_image():
    image_data= request.get_json()
    conn= psycopg2.connect(database="mytestdb",
                       user="postgres",
                       password="123456",
                       host="localhost",
                       port="5432")

    cur = conn.cursor()

    final_image=image_data['ImagePath']
    # print(final_image)
    course_num= image_data['ImageId']
    # print(course_num)

    cur.execute('''UPDATE public."ImageApp_images" SET "ImagePath"=%s WHERE "ImageId"=%s;''',(final_image,course_num))
    conn.commit()
    cur.close()
    conn.close()

    return {"message":"updated successfully"}, 201    

@app.delete("/delete/<course_num>")
def delete_entry(course_num):

    conn= psycopg2.connect(database="mytestdb",
                       user="postgres",
                       password="123456",
                       host="localhost",
                       port="5432")

    cur = conn.cursor()


    cur.execute('''DELETE FROM public."ImageApp_images" WHERE "ImageId"=%s;''',(course_num))
    conn.commit()
    cur.close()
    conn.close()

    return {"message":"deleted successfully"}, 200



# api.add_resource(Video,"/data/<int:course_num>")
if __name__=='__main__':
    app.run(debug=True)