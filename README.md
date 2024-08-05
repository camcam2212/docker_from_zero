# Hướng dẫn cài đặt và làm quen với Docker/Apache Airflow cho các bạn DA/BI

<!-- ![Mô tả](./images/description1.png) -->

## Mục đích
Hướng tới DA fullstack, có thể ETL dữ liệu từ A -> Á, phân tích, đưa ra insight,... 


## Các File Chính

1. **docker-compose.yaml**: 
   - File này giúp tạo và quản lý các container của ứng dụng qua 1 tệp duy nhất. Định nghĩa các cấu hình, dịch vụ, thiết lập mạng, container,...

2. **Dockerfile**:
   - File này hỗ trợ bổ sung thêm nguyên liệu, hương vị cho miếng bánh ban đầu bạn xây dựng,, ví dụ cài thêm thư viện, volumn,...

3. **requirements.txt**:
   - File này chứa các thư viện bạn muốn cài thêm mà trong container Worker không có sẵn

4. **create_table_postgresql**:
   - Câu lệnh tạo view mẫu trên psql db, sau ace copy cho tiện

5. **docker_build_image.txt**:
   - Câu lệnh build image khó nhớ :D

   
## Các bước thực hiện

BƯỚC 1. **Tải/cài đặt docker desktop**:
   - [Download tùy theo hệ điều lành của máy tính](https://www.docker.com/products/docker-desktop/)

BƯỚC 2. **TUrn on WSL2**:
   - [Đối với Windows](https://learn.microsoft.com/en-us/windows/wsl/install)
   - HĐH Linux <MacOS,Ubuntu> k cần quan tâm
   - Chi tiết:
    + Open Terminal/PowerShell by Admin
    + "wsl --install" 
    + Done

BƯỚC 3. **Mở Docker-desktop**:
   - Đi đến thư mục lưu folder vừa tải về
   - "docker compose up -d" để khởi tạo

BƯỚC 4. **Cài đặt pgadmin4 (công cụ quản trị database)**:
   - "docker pull dpage/pgadmin4"

## Yêu Cầu Hệ Thống
- Laptop
- Nhiệt huyết tìm hiểu và mong muốn trở thành vua của ngành dữ liệu

## Người phát triển
Sondn <3
