# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class TokenContract(gl.Contract):
    # State variables: TreeMap và u256 là bắt buộc cho Storage
    total_supply: u256
    balances: TreeMap[str, u256]

    def __init__(self, initial_supply: u256):
        self.total_supply = initial_supply
        self.balances = TreeMap()
        
        # FIX CỐT LÕI: Sử dụng gl.get_caller() để lấy address người deploy
        # Đây là hàm chuẩn duy nhất trong v0.2.16
        deployer = gl.get_caller()
        self.balances[deployer] = initial_supply

    @gl.public.view
    def get_balance_of(self, address: str) -> u256:
        return self.balances.get(address, u256(0))

    @gl.public.write
    def transfer(self, to_address: str, amount: u256):
        """
        Giao dịch chuyển tiền được giám sát bởi AI Guardian.
        """
        sender = gl.get_caller()
        sender_balance = self.balances.get(sender, u256(0))

        # 1. Kiểm tra số dư (SMC logic)
        assert sender_balance >= amount, "Lỗi: Số dư không đủ"

        # 2. AI Validator (Kiểm tra ý đồ giao dịch)
        prompt = (
            f"Phân tích giao dịch: Ví {sender} gửi {amount} token đến {to_address}. "
            f"Địa chỉ nhận có dấu hiệu lừa đảo hoặc giao dịch có bất thường không? "
            f"Trả về 'SAFE' hoặc 'SUSPICIOUS'."
        )
        
        # AI request sẽ kích hoạt Optimistic Democracy
        security_verdict = self.ai_request(prompt)

        if "SUSPICIOUS" in security_verdict.upper():
            assert False, f"Giao dịch bị chặn bởi AI Guardian. Lý do: {security_verdict}"

        # 3. Thực thi chuyển tiền (Atomic Transition)
        self.balances[sender] = sender_balance - amount
        
        receiver_balance = self.balances.get(to_address, u256(0))
        self.balances[to_address] = receiver_balance + amount
