---
name: calculator
track: core
kind: local_formatter
provider: local
requires_env: []
inputs: [expression]
outputs: [tool, expression, result]
side_effect: false
requires_confirmation: false
---
# calculator

Thực hiện biểu thức số học bằng AST: `+`, `-`, `*`, `/`, `//`, `%` (chia lấy dư), `**` và ngoặc đơn.
Phần trăm phải viết thành tỷ lệ, ví dụ tăng 15% là `120 * 1.15`; không hỗ trợ cú pháp `15%` đứng riêng.
Giữ chính xác số nguyên, làm tròn kết quả số thực đến 6 chữ số thập phân. Không dùng cho tính toán tài chính cần độ chính xác thập phân tuyệt đối.
Chỉ nhận chuỗi chứa số và phép toán; từ chối boolean, tên biến, lời gọi hàm và kết quả không hữu hạn. Giới hạn 512 ký tự, 128 AST nodes, số mũ tối đa 1000 và số nguyên tối đa 4096 bit để hạn chế chi phí tính toán.
Trả về kết quả số hoặc dictionary chứa thông tin lỗi nếu biểu thức không hợp lệ.
