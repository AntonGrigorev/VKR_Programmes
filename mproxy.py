#!/usr/bin/python3
from mitmproxy import http, ctx
from datetime import datetime
import logging
import tensorflow as tf
from tensorflow import keras
import numpy as np
import urllib.parse
import os
import os

log_path = "/home/anton/programms/mitmproxy_requests.log"

if not os.path.exists(log_path):
    with open(log_path, "w", encoding="utf-8"):
        pass  

model = tf.keras.models.load_model('/home/anton/programms/model.h5')

def write_to_file(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/home/anton/programms/mitmproxy_requests.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")



def url_decode(encoded_URL):
  return urllib.parse.unquote(encoded_URL)

def load_data(data, max_length=1000):
    url = data.lower()  
    url_list = []
    decoded_url = url_decode(url)  
    encoded_url = [ord(x) for x in str(decoded_url).strip()]
    encoded_url = encoded_url[:max_length]
    url_len = len(encoded_url)
    if url_len < max_length:
        encoded_url += ([0] * (max_length - url_len))
    url_list.append((encoded_url))
    url_list = np.array(url_list)
    return url_list

class RequestModifier:
    def request(self, flow: http.HTTPFlow) -> None:

        ctx.log.info(f"Original request to: {flow.request.url}")

        if flow.request.method == "POST" and flow.request.content:
            original_body = flow.request.content.decode("utf-8")
            #flow.request.content = original_body.encode("utf-8")
            model_input = load_data(original_body)
            answer = model.predict(model_input)
            answer = answer.ravel().tolist()
            if(answer[0]>=0.5):

                final_ans = 1
            else:

                final_ans = 0
            #print('first is '+str(answer[0])+' final ans is '+str(final_ans)+'\n')
            if(final_ans == 0):
                write_to_file(f"{original_body} Normal")
            else:
                write_to_file(f"{original_body} Malicious") 
addons = [RequestModifier()]
