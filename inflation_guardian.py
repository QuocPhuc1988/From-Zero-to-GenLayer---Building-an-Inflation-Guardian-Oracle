from genlayer import IntelligentContract

class InflationGuardian(IntelligentContract):
    def __init__(self, fixed_salary: int):
        self.fixed_salary = fixed_salary # Mức lương cố định (Assets)
        self.status = "Normal"

    @view
    def evaluate_pressure(self):
        """
        AI quét giá xăng RON 95 và giá gạo để đánh giá áp lực chi tiêu.
        """
        # Đây là nơi Optimistic Democracy hoạt động
        prompt = f"""
        Hôm nay là 28/03/2026. Hãy tìm giá xăng RON 95 và giá gạo tại Kiên Giang, Việt Nam.
        Với mức thu nhập cố định là {self.fixed_salary} VND.
        Hãy đánh giá áp lực chi tiêu: 'An toàn' hoặc 'Cảnh báo'.
        Chỉ trả về 1 từ duy nhất.
        """
        prediction = self.ai_request(prompt)
        
        if "Cảnh báo" in prediction:
            self.status = "WARNING: Inflation Crisis"
        else:
            self.status = "Normal"
            
        return self.status
