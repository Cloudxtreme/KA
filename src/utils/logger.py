import logging

_ = logging.getLogger()

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

_.setLevel(logging.DEBUG)
_.addHandler(handler)

