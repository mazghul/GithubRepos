from threading import Thread
from helpers import *


class StargazerWorker(Thread):
    """
    A class that initializes execution of threading
    """

    def __init__(self, queue):
        """

        :param queue:
        """
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        """

        :return:
        """
        while True:
            data = self.queue.get()
            page, organizations_url, organizations_repos_url_extension, per_page, headers, repos = data
            try:
                get_repos(page, organizations_url, organizations_repos_url_extension, per_page, headers, repos)
            except Exception as error:
                print(error)
            finally:
                self.queue.task_done()
