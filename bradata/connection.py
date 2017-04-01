import tqdm
import time
import requests


class Connection:
    """
    Class that handle connections
    """

    def perform_request(self, url, nr_tries=5, binary=False):
        """
        Perform a request handling exception and server errors printing status

        :param url: string
        :param nr_tries: int
        :return: dict :: status : ok/error, content: xml/url, [error_type, error_desc] if error
        """
        count = 0
        while True:
            try:
                print('Fetch {}'.format(url))

                #fetch_time = time.time()
                req = requests.get(url, timeout=1)
                #fetch_time = time.time() - fetch_time

                status = req.status_code
                if status != 200:
                    print('ERROR {}. {}'.format(req.status_code, req.text))
                    time.sleep(5)

                    count += 1
                    if count > nr_tries:
                        print('Too many errors in a row. Returned: ERROR {}'.format(req.status_code))
                        return {'status': 'error', 'error_type': req.status_code, 'error_desc': req.text, 'content': url}

                    print('Trying Again...')
                    continue

                else:
                    if binary:
                        return {'status': 'ok', 'content': req.content}
                    else:
                        return {'status': 'ok', 'content': req.text}

            except Exception as e:

                print('EXCEPTION {}'.format(e))

                count += 1
                if count > nr_tries:
                    print('Too many exceptions in a row. Returned: ERROR EXC')
                    return {'status': 'error', 'error_type': 'exception', 'error_desc': e, 'content': url}

                time.sleep(5)
                print('Trying Again...')
                continue
