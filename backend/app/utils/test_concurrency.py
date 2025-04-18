import asyncio
import httpx

# API endpoint URL
API_URL = "http://localhost:8000/chat"

# First test payload
payload_1 = {
    "phase": "qa",
    "user_info": {
        "HMO name": "מכבי",
        "Insurance membership tier": "זהב"
    },
    "messages": [{"role": "user", "content": "מה ההנחה על סתימה?"}]
}

# Second test payload
payload_2 = {
    "phase": "qa",
    "user_info": {
        "HMO name": "מאוחדת",
        "Insurance membership tier": "כסף"
    },
    "messages": [{"role": "user", "content": "מה ההנחה על בדיקות ראייה?"}]
}

async def send_request(payload):
    """
    Sends an asynchronous POST request with the given payload and prints the response.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload)
        print(response.json())

async def main():
    """
    Test that runs multiple requests concurrently.
    """
    await asyncio.gather(
        send_request(payload_1),
        send_request(payload_2)
    )

if __name__ == "__main__":
    asyncio.run(main())
