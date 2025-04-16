import asyncio
import httpx

API_URL = "http://localhost:8000/chat"

payload_1 = {
    "phase": "qa",
    "user_info": {
        "HMO name": "מכבי",
        "Insurance membership tier": "זהב"
    },
    "messages": [{"role": "user", "content": "מה ההנחה על סתימה?"}]
}

payload_2 = {
    "phase": "qa",
    "user_info": {
        "HMO name": "מאוחדת",
        "Insurance membership tier": "כסף"
    },
    "messages": [{"role": "user", "content": "מה ההנחה על בדיקות ראייה?"}]
}

async def send_request(payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload)
        print(response.json())

async def main():
    await asyncio.gather(
        send_request(payload_1),
        send_request(payload_2)
    )

if __name__ == "__main__":
    asyncio.run(main())
