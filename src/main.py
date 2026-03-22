import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def run(self):
        self.logger.debug('Debugging information')
        self.logger.info('Informational message')
        self.logger.warning('Warning message')
        self.logger.error('Error message')
        self.logger.critical('Critical message')

if __name__ == '__main__':
    app = App()
    app.run()