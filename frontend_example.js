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
