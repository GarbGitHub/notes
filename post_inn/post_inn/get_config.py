import environ
env = environ.Env()
environ.Env.read_env()

GET_CONFIG = env('GET_CONFIG')
