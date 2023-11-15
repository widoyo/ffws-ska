import logging
import sys
import datetime
from zoneinfo import ZoneInfo

import daemonocle
import paho.mqtt.client as mqtt
import telebot
from flask import json

from app.models import Logger, Pos, Hourly, db_wrapper

# TOKEN = 6487123731:AAFCzFK2Xi1BHZ8F6NQQWP9KxyY-i5SuzjM (@pupr_ska_bot)
# chat_id = -1002010036857 (FFWS Kota Surakarta Group)
# channel_chat_id = -1002136462883 (FFWS Kota Surakarta Channel)

TOKEN = "6487123731:AAFCzFK2Xi1BHZ8F6NQQWP9KxyY-i5SuzjM"
ffws_ska_chat_id = -1002136462883
alarm_msg = '\[*SIAGA {level}*\] Lokasi *{lokasi}* pada {waktu}'

def on_connect(client, userdata, flags, rc):
    client.subscribe("dpuprska")
    
def on_message(client, userdata, msg):
    '''
    1. update 'logger' field: latest_sampling, latest_battery, latest_up
    2. upsert 'hourly' field: num_data, rain/wlevel
    '''
    data = json.loads(msg.payload)
    logging.debug(msg.topic + " " + data.get('device'))
    try:
        sn = data.get('device').split('/')[1]
    except:
        return
        
    proses_message(sn, data)
    
    #if data.get('alarm') > 0:
    print(msg.topic + " " + str(msg.payload))
    
def proses_message(sn: str, data: dict):
    # update data terbaru logger
    logger = Logger.get(sn=sn)
    logger.latest_sampling = data.get('sampling')
    logger.latest_up = data.get('up_since')
    logger.latest_battery = data.get('battery')
    logger.save()

    # kirim alert jika perlu
    if data.get('alarm_level', None):
        if data.get('alarm_level') > 0:
            loc = {'2309-1': 'Kedung Belang', '2309-2': 'Gandekan', '2309-3': 'Joyotakan Timur'}
            our_text = alarm_msg.format(**
                {'level': data.get('alarm_level') or 0, 
                'lokasi': loc.get(data.get('device').split('/')[1]), 
                'waktu': datetime.datetime.fromtimestamp(
                    data.get('sampling'), ZoneInfo('Asia/Jakarta')).strftime('%H:%M, %d %b')})
            test_telegrambot(our_text)
    
    # upsert into hourly
    hour = data.get('sampling') - (data.get('sampling') % 3600)
    pos = Pos.get(logger.pos_id)
    tick = data.get('tick', None)
    distance = data.get('distance', None)
    hourly, created = Hourly.get_or_create(pos_id=pos.id, sampling=hour, 
                                  defaults={'num_data': 1,
                                            'tick': tick,
                                            'distance': distance, 
                                            'rain': 0, 
                                            'wlevel': 0,
                                            'num_alarm': 0})
    if not created:
        hourly.num_data += 1
        if tick:
            try:
                hourly.tick += tick
            except:
                hourly.tick = tick
        if distance:
            hourly.distance = distance
                
    
    
def cb_shutdown(message, code):
    logging.info('Daemon is stopping')
    logging.debug(message)

def main():
    logging.info('Daemon starting')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.prinus.net", 14983, 60)

    client.loop_forever()
    
def run_daemon():
    daemon = daemonocle.Daemon(
        worker=main,
        shutdown_callback=cb_shutdown,
        pid_file='/tmp/mydaemon.pid'
    )
    daemon.do_action(sys.argv[1])

def test_telegrambot(msg:str):
    tb = telebot.TeleBot(TOKEN)
    
    #tb.send_message(chat_id=-1002010036857, text="<b>Hello</b>", parse_mode='HTML')
    tb.send_message(chat_id=ffws_ska_chat_id, text=msg, parse_mode='MarkdownV2')
    
if __name__ == '__main__':
    from . import DATABASE, create_app
    logging.basicConfig(filename='/tmp/mydaemon.log', 
                        level=logging.DEBUG, 
                        format='%(asctime)s [%(levelname)s] %(message)s')
    app = create_app()
    l = Logger.get(sn='2309-1')
    logging.debug('LOGER 2309-1')
    run_daemon()
