# From Zero to GenLayer: Building an Inflation Guardian Oracle

Chào mừng bạn đến với hướng dẫn xây dựng dApp đầu tiên trên GenLayer! Trong bài này, chúng ta sẽ tạo ra một **Inflation Guardian** (Người Bảo Vệ Lạm Phát) - một Intelligent Contract có khả năng tự động đánh giá áp lực kinh tế thực tế dựa trên dữ liệu thế giới thực.

## Giới thiệu
GenLayer cho phép bạn viết các hợp đồng thông minh bằng Python có khả năng tương tác với AI và dữ liệu Internet một cách phi tập trung (thông qua Optimistic Democracy).

## 1. Viết Intelligent Contract (Python)
Đây là phần "linh hồn" của dApp. File `inflation_guardian.py` chứa logic đánh giá áp lực chi tiêu dựa trên giá xăng và giá gạo.

```python
from genlayer import IntelligentContract

class InflationGuardian(IntelligentContract):
    def __init__(self, fixed_salary: int):
        self.fixed_salary = fixed_salary # Mức lương cố định (VND)
        self.status = "Normal"

    @view
    def evaluate_pressure(self):
        """
        AI quét giá xăng RON 95 và giá gạo để đánh giá áp lực chi tiêu.
        """
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
```

## 2. Tương tác Frontend (genlayer-js)
Sau khi deploy contract, bạn có thể dễ dàng đọc trạng thái từ ứng dụng web của mình:

```javascript
import { GenLayer } from 'genlayer-js';

const client = new GenLayer();
const contractAddress = 'YOUR_CONTRACT_ADDRESS';

async function checkInflationStatus() {
  const status = await client.readContract({
    address: contractAddress,
    functionName: 'evaluate_pressure',
  });
  console.log("Trạng thái kinh tế của bạn:", status);
}
```

## Cách hoạt động
1. **Lương cố định**: Bạn khởi tạo contract với mức thu nhập hàng tháng.
2. **AI Request**: Khi gọi hàm `evaluate_pressure`, GenLayer sẽ yêu cầu AI tìm kiếm dữ liệu giá cả thực tế tại Việt Nam.
3. **Đánh giá**: AI so sánh mức lương với chi phí sinh hoạt (xăng, gạo) và đưa ra cảnh báo nếu lạm phát quá cao.

---
*Hướng dẫn thực hiện bởi Antigravity.*
