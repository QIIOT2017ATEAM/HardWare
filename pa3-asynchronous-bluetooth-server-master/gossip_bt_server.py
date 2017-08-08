from btserver import BTServer
from bterror import BTError

import argparse
import asyncore
import json
from random import uniform
from threading import Thread
from time import sleep, time
import datetime

if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="csv", help="set output format: csv, json")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "GossipBTServer"
    server = BTServer(uuid, service_name)

    # Create the server thread and run it
    server_thread = Thread(target=asyncore.loop, name="Gossip BT Server Thread")
    server_thread.daemon = True
    server_thread.start()

    while True:
        for client_handler in server.active_client_handlers.copy():
            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"


            #temp
            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            v=5*0.000244140625*raw
###

            epoch_time = int(time())    # epoch time   @@normal
            real_time = datetime.datetime.now()
            temp = (1000*v)-642      # random temperature
            SN1 = uniform(23, 28)       # random SN1 value
            SN2 = uniform(16, 30)       # random SN2 value
            SN3 = uniform(25, 40)       # random SN3 value
            SN4 = uniform(30, 55)     # random SN4 value
            PM25 = uniform(40, 55)    # random PM25 value


            msg = ""
            if args.output_format == "csv":   #@@@ we dont use this form
                msg = "%f, %d, %f, %f, %f, %f, %f, %f" % (real_time, "0", SN1, SN2, SN3, SN4, PM25)
            elif args.output_format == "json":
                output = {'MAC' : '5C:31:3E:29:55:BC'
                          'type': '1',       # 1=currently time / 2=history time
                          'time': epoch_time,
                          'temp': round(temp,2),
                          'CO': round(SN1,2),
                          'NO2': round(SN2,2),
                          'SO2': round(SN3,2),
                          'O3': round(SN4,2),
                          'PM25': round(PM25,2)}
                msg = json.dumps(output)
            try:
                client_handler.send(msg + '\n')
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()
    #testtestestestet
            # Sleep for 3 seconds
        sleep(3)
