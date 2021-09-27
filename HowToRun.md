1. Phải chạy lệnh này trước: redis-server --daemonize yes (chạy 1 lần)
2. Chạy chấm bài: celery -A uteoj worker -Q uteoj_judger -Ofair
3. Chay nen he thong: celery -A uteoj worker -Q uteoj_system -Ofair