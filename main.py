import threading

from fastapi import FastAPI
import generater
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello MDG"}

def start_server():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# 메인 서버 실행
def main():
    start_server()

def start_log_thread():
    # 랜덤 로그 생성 쓰레드
    log_thread = threading.Thread(target=generater.generate_log, daemon=True)
    log_thread.start()

if __name__ == "__main__":
    main()
    start_log_thread()