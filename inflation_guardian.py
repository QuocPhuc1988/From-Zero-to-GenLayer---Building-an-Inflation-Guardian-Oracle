# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class TokenContract(gl.Contract):
    # Khai báo State Variables
    total_supply: u256
    balances: TreeMap[str, u256]

    def __init__(self, initial_supply: u256):
        """
        Khởi tạo Token và cấp toàn bộ Supply cho người Deploy.
        """
        self.total_supply = initial_supply
        self.balances = TreeMap()
        
        # Gán toàn bộ số dư ban đầu cho người tạo hợp đồng
        self.balances[gl.message.sender] = initial_supply

    @gl.public.view
    def get_balance_of(self, address: str) -> u256:
        """
        Kiểm tra số dư của một địa chỉ bất kỳ.
        """
        return self.balances.get(address, u256(0))

    @gl.public.write
    def transfer(self, to_address: str, amount: u256):
        """
        Logic chuyển tiền an toàn: Kiểm tra số dư -> Trừ người gửi -> Cộng người nhận.
        """
        sender = gl.message.sender
        
        # 1. Lấy số dư hiện tại của người gửi
        sender_balance = self.balances.get(sender, u256(0))
        
        # 2. Kiểm tra điều kiện (Security First)
        # Nếu không đủ tiền, giao dịch sẽ fail và không tốn Gas/Tài nguyên vô ích
        assert sender_balance >= amount, "Lỗi: Số dư không đủ để thực hiện giao dịch"
        
        # 3. Cập nhật số dư người gửi
        self.balances[sender] = sender_balance - amount
        
        # 4. Cập nhật số dư người nhận
        receiver_balance = self.balances.get(to_address, u256(0))
        self.balances[to_address] = receiver_balance + amount
        
        # Log đơn giản để xác nhận (Tùy chọn)
        print(f"Giao dịch thành công: {amount} token đã được gửi tới {to_address}")
