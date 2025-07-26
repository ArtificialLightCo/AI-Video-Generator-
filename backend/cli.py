# backend/cli.py
import argparse
from backend.model_manager import ModelManager
from backend.prompt_assistant import PromptAssistant
from backend.preview import Previewer
from backend.stt import SpeechToText
from backend.orchestration import Orchestrator

def main():
    parser = argparse.ArgumentParser('Ultimate AI Video Generator')
    parser.add_argument('--prompt', help='Text prompt or scenes delimited by "|"')
    parser.add_argument('--stt-audio', help='Optional audio file for STT prompt')
    parser.add_argument('--init-image', help='Optional image to guide generation')
    parser.add_argument('--duration', type=int, required=True,
                        help='Video duration in seconds (max 1200)')
    parser.add_argument('--output', required=True,
                        help='Path to save the final MP4')
    parser.add_argument('--style', default=None,
                        help='Optional LUT file for color grading')
    parser.add_argument('--music', default=None,
                        help='Optional background music file path')
    parser.add_argument('--particles', action='store_true',
                        help='Enable confetti overlay')
    parser.add_argument('--title-text', default=None,
                        help='Animated title text overlay')
    parser.add_argument('--shake', action='store_true',
                        help='Enable camera shake effect')
    parser.add_argument('--interp', type=int, default=1,
                        help='Frame interpolation factor (e.g. 2 → double FPS)')
    parser.add_argument('--assist', action='store_true',
                        help='Refine prompt via on-device LLM')
    parser.add_argument('--preview', action='store_true',
                        help='Show low-res preview while generating')
    parser.add_argument('--download-models', action='store_true',
                        help='Pre-fetch all required models')
    args = parser.parse_args()

    # Cap duration to 20 minutes
    MAX_DUR = 1200
    if args.duration > MAX_DUR:
        print(f"⚠️ Duration too long; capping to {MAX_DUR}s")
        args.duration = MAX_DUR

    # 1) Model management
    mm = ModelManager(cache_dir='models')
    if args.download_models:
        print("📥 Downloading AI models…")
        mm.download('damo-vilab/modelscope-text-to-video-synthesis')
        mm.download('stabilityai/stable-video-diffusion-img2vid-xt')
        print("✅ Models ready")

    # 2) STT transcription if provided
    prompt = args.prompt
    if not prompt and args.stt_audio:
        stt = SpeechToText()
        print("🎤 Transcribing prompt from audio…")
        prompt = stt.transcribe(args.stt_audio)
        print("📝 Prompt:", prompt)

    # 3) Prompt assistance
    if args.assist and prompt:
        pa = PromptAssistant(model_path='models/llm/ggml-gpt4all.bin')
        print("🤖 Refining prompt…")
        prompt = pa.suggest(prompt)
        print("📝 Refined prompt:", prompt)

    # 4) Low-res preview
    if args.preview and prompt:
        print("👀 Starting low-res preview (Ctrl+C to stop)…")
        prev = Previewer(model_name='stabilityai/stable-video-diffusion-img2vid-xt')
        prev.start(prompt)
        input("Press Enter to stop preview…")
        prev.stop()

    # Ensure models are cached
    mm.download('damo-vilab/modelscope-text-to-video-synthesis')
    mm.download('stabilityai/stable-video-diffusion-img2vid-xt')

    # 5) Generate full video
    orch = Orchestrator()
    out = orch.create_video(
        prompt=prompt,
        total_duration=args.duration,
        output_path=args.output,
        style=args.style,
        music_path=args.music,
        interpolate_factor=args.interp,
        init_image=args.init_image,
        particles=args.particles,
        title_text=args.title_text,
        camera_shake=args.shake
    )

    print(f"🎉 Final video saved at: {out}")

if __name__ == '__main__':
    main()
