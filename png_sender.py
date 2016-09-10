import httplib, urllib
import time
import base64
import json


def send_post(server, port, data):
    headers = {"Content-type": "application/json"}
    conn = httplib.HTTPConnection('{0}:{1}'.format(server, port), timeout=1.0)
    conn.request("POST", "/image", data, headers)
    response = conn.getresponse()
    print response.status, response.reason

    data = response.read()
    print 'got response:', data
    conn.close()


def main(server, port, contributor):
    
    while True:
        try:
            with open('out.png', 'rb') as f:
                data = f.read()

            post_data = {'contributor-id': contributor,
                         'image': base64.b64encode(data)}
            send_post(server, port, json.dumps(post_data))
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print e

        # Sleep some time
        time.sleep(1)
    
if __name__ == '__main__':
    
    server = "192.168.43.224"
    port = 8080
    contributor = 'cam1'
    main(server, port, contributor)
