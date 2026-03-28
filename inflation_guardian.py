# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *

class TokenContract(gl.Contract):
    # Khai báo State với TreeMap và u256
    total_supply: u256
    balances: TreeMap[str, u256]

    def __init__(self, initial_supply: u256):
        self.total_supply = initial_supply
        self.balances = TreeMap()
        
        # FIX CỐT LÕI: Sử dụng gl.get_caller_address() 
        # để gán toàn bộ supply cho người deploy
        deployer = gl.get_caller_address()
        self.balances[deployer] = initial_supply

    @gl.public.view
    def get_balance_of(self, address: str) -> u256:
        return self.balances.get(address, u256(0))

    @gl.public.write
    def transfer(self, to_address: str, amount: u256):
        # Sử dụng gl.get_caller_address() cho mọi logic xác thực
        sender = gl.get_caller_address()
        sender_balance = self.balances.get(sender, u256(0))

        assert sender_balance >= amount, "Lỗi: Số dư không đủ"

        # Cập nhật số dư (Atomic Swap)
        self.balances[sender] = sender_balance - amount
        
        receiver_balance = self.balances.get(to_address, u256(0))
        self.balances[to_address] = receiver_balance + amount
