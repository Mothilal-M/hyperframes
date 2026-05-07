import asyncio
import json
import edge_tts

VOICE = "en-US-GuyNeural"
RATE = "+0%"

async def main():
    with open("narration.txt", "r", encoding="utf-8") as f:
        text = f.read()

    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    sentences = []
    with open("narration.mp3", "wb") as audio_out:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_out.write(chunk["data"])
            elif chunk["type"] == "SentenceBoundary":
                start = chunk["offset"] / 1e7
                end = (chunk["offset"] + chunk["duration"]) / 1e7
                sentences.append({
                    "text": chunk["text"],
                    "start": round(start, 3),
                    "end": round(end, 3),
                })

    with open("transcript.json", "w", encoding="utf-8") as f:
        json.dump(sentences, f, indent=2)

    if sentences:
        print(f"done: {len(sentences)} sentences, last ends at {sentences[-1]['end']:.2f}s")
    else:
        print("done: no boundaries returned")

asyncio.run(main())
