import os
def run():
    os.system('uvicorn app.main:app --reload')


if __name__ == '__main__':
    print(os.getcwd())
    run()