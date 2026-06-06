# voice.py
import edge_tts
import asyncio
import os
import threading

KALAM_VOICE = "en-IN-PrabhatNeural"

def speak_fast(text, output_path="memory/response.mp3"):
    """
    Generates speech using edge-tts.
    Handles asyncio event loop conflicts with Streamlit.
    """
    try:
        os.makedirs("memory", exist_ok=True)
        text = text[:300]

        result = [None]
        exception = [None]

        def run_in_thread():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                async def generate():
                    communicate = edge_tts.Communicate(text, KALAM_VOICE)
                    await communicate.save(output_path)
                    return output_path
                
                result[0] = loop.run_until_complete(generate())
                loop.close()
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join(timeout=30)

        if exception[0]:
            print(f"TTS error: {exception[0]}")
            return None

        return result[0]

    except Exception as e:
        print(f"Voice error: {e}")
        return None