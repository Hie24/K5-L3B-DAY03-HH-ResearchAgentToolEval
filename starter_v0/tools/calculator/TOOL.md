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

Thực hiện tính toán an toàn các biểu thức số học cơ bản (cộng, trừ, nhân, chia, lũy thừa, phần trăm).
Trả về kết quả số hoặc dictionary chứa thông tin lỗi nếu biểu thức không hợp lệ.
