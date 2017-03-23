import requests
import time

class Connection():

    def perform_request(self, url, n_of_tentatives=5):
        """
        Perform a request handling exception and server errors printing status

        :param url: string
        :param n_of_tentatives: int
        :return: dict :: status : ok/error, content: xml/url, [error_type, error_desc if error]
        """

        count = 0
        while 1:
            try:
                print('Fetch {}'.format(url))

                #fetch_time = time.time()
                req = requests.get(url, timeout=60)
                #fetch_time = time.time() - fetch_time

                status = req.status_code
                if status != 200:
                    print('ERROR {}. {}'.format(req.status_code, req.text))
                    time.sleep(5)

                    count += 1
                    if count > n_of_tentatives:
                        print('Too many errors in a row. Returned: ERROR {}'.format(req.status_code))
                        return {'status': 'error', 'error_type': req.status_code, 'error_desc': req.text, 'content': url}

                    print('Trying Again...')
                    continue

                else:
                    return {'status': 'ok', 'content': req.text}

            except Exception as e:

                print('EXCEPTION {}'.format(e))

                count += 1
                if count > n_of_tentatives:
                    print('Too many exceptions in a row. Returned: ERROR EXC')
                    return {'status': 'error', 'error_type': 'exception', 'error_desc': e, 'content': url}

                time.sleep(5)
                print('Trying Again...')
                continue

