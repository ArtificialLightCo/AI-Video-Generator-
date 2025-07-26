# backend/preview.py
import threading
import time
import torch
from diffusers import DiffusionPipeline

class Previewer:
    """
    Low-res previewer: generates a single frame periodically
    to give visual feedback during long renders.
    """
    def __init__(
        self,
        model_name: str = 'stabilityai/stable-video-diffusion-img2vid-xt',
        device: str = None
    ):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.pipe = DiffusionPipeline.from_pretrained(model_name).to(self.device)
        self.thread = None
        self.stop_event = threading.Event()

    def _preview_loop(self, prompt: str):
        while not self.stop_event.is_set():
            out = self.pipe(prompt, num_inference_steps=10)
            img = out.images[0]
            img.show()
            time.sleep(1)

    def start(self, prompt: str):
        """
        Begin asynchronous preview. Call stop() to end.
        """
        self.stop_event.clear()
        self.thread = threading.Thread(
            target=self._preview_loop,
            args=(prompt,),
            daemon=True
        )
        self.thread.start()

    def stop(self):
        """
        Stop the preview loop.
        """
        self.stop_event.set()
        if self.thread:
            self.thread.join()
