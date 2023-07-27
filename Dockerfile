# # Sử dụng một hình ảnh cơ sở Python
# FROM python:3.9

# # Đặt thư mục làm việc
# WORKDIR /app

# # Sao chép tệp requirements.txt và cài đặt các dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# # Sao chép mã nguồn của ứng dụng Django vào hình ảnh
# COPY . .

# # Thiết lập các biến môi trường
# ENV MYSQL_HOST=localhost \
#     MYSQL_PORT=3306 \
#     MYSQL_DB=shoponline \
#     MYSQL_USER=root \
#     MYSQL_PASSWORD=''

# # Chạy các migrations
# RUN python manage.py migrate

# # Theo dõi cổng 8000
# EXPOSE 8000

# # Chạy ứng dụng Django
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
