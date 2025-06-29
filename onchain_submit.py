from web3 import Web3

# ===== 1. 输入私钥与目标地址 =====
PRIVATE_KEY = input("🔐 请输入你的私钥（用于签名，建议创建小号地址）：\n> ").strip()
TARGET_ADDRESS = input("📍 请输入你要发送到的地址（一般是你自己）：\n> ").strip()

# ===== 2. 配置 RPC =====
RPC_URL = "https://mainnet.base.org"  # 可替换为其他EVM链
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
print(f"\n✅ 当前发送地址：{account.address}")

# ===== 3. 输入上链内容 =====
idea = input("\n💡 请输入你要上链的文本内容（任意文本/表情均可）：\n> ").strip()
hex_data = idea.encode("utf-8").hex()
final_data = "0xaa00" + hex_data  # 自定义识别前缀（可改）

# ===== 4. 构造交易 & 预估 gas =====
nonce = w3.eth.get_transaction_count(account.address)
gas_price = w3.eth.gas_price
tx = {
    "to": TARGET_ADDRESS,
    "value": 0,
    "data": final_data,
    "gasPrice": gas_price,
    "nonce": nonce,
    "chainId": 8453  # Base链ID，可改
}

try:
    estimated_gas = w3.eth.estimate_gas({
        "from": account.address,
        "to": tx["to"],
        "data": tx["data"],
        "value": 0
    })
    fee_eth = w3.from_wei(estimated_gas * gas_price, 'ether')

    print(f"\n🚀 将上链内容：{idea}")
    print(f"📦 Data 大小：{len(hex_data) // 2} 字节")
    print(f"🔢 预估 Gas：{estimated_gas}")
    print(f"💰 预估费用：{fee_eth:.6f} BASE")

    confirm = input("是否发送？（y/n）: ").strip().lower()
    if confirm != "y":
        print("❌ 已取消发送。")
        exit()

    tx["gas"] = estimated_gas
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"✅ 已发送！交易哈希：{tx_hash.hex()}")

except Exception as e:
    print(f"❌ 发送失败：{e}")
