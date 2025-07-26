# 1. Make sure the folder exists
mkdir -p backend

# 2. Create the file and start pasting
cat > backend/cli.py << 'EOF'
# cli.py
import argparse
from backend.model_manager import ModelManager
from backend.prompt_assistant import PromptAssistant
from backend.preview import Previewer
from backend.orchestration import Orchestrator

def main():
    parser = argparse.ArgumentParser('Ultimate AI Video Generator')
    parser.add_argument(
        '--prompt', required=True,
        help='Text prompt or scenes delimited by "|"'
    )
    parser.add_argument(
        '--duration', type=int, required=True,
        help='Total video duration in seconds (max 1200)'
    )
    parser.add_argument(
        '--output', required=True,
        help='Path to save the final MP4'
    )
    parser.add_argument(
        '--style', default=None,
        help='Optional LUT file for color grading'
    )
    parser.add_argument(
        '--music', default=None,
        help='Optional background music file path'
    )
    parser.add_argument(
        '--interp', type=int, default=1,
        help='Frame interpolation factor (e.g. 2 → double FPS)'
    )
    parser.add_argument(
        '--assist', action='store_true',
        help='Refine prompt via on-device LLM'
    )
    parser.add_argument(
        '--preview', action='store_true',
        help='Show live low-res preview as it generates'
    )
    parser.add_argument(
        '--download-models', action='store_true',
        help='Fetch all needed models before running'
    )
    args = parser.parse_args()

    # Enforce maximum duration
    MAX_DUR = 1200  # seconds (20 minutes)
    if args.duration > MAX_DUR:
        print(f"⚠️ Duration {args.duration}s exceeds max {MAX_DUR}s; capping to {MAX_DUR}s")
        args.duration = MAX_DUR

    # 1) Model management
    mm = ModelManager(cache_dir='models')
    if args.download_models:
        print("📥 Downloading required models…")
        mm.download('damo-vilab/modelscope-text-to-video-synthesis')
        mm.download('stabilityai/stable-video-diffusion-img2vid-xt')
        print("✅ Models downloaded.")

    # 2) Prompt refinement via on-device LLM
    prompt = args.prompt
    pa = PromptAssistant(model_path='models/llm/ggml-gpt4all.bin')
    if args.assist:
        print("🤖 Refining prompt with on-device LLM…")
        prompt = pa.suggest(prompt)
        print("📝 Refined prompt:", prompt)

    # 3) Real-time low-res preview
    if args.preview:
        print("👀 Starting low-res preview… (press Enter to stop)")
        previewer = Previewer(model_name='stabilityai/stable-video-diffusion-img2vid-xt')
        previewer.start(prompt)
        input()
        previewer.stop()
        print("⏹ Preview stopped.")

    # Ensure models are cached before full run
    mm.download('damo-vilab/modelscope-text-to-video-synthesis')
    mm.download('stabilityai/stable-video-diffusion-img2vid-xt')

    # 4) Full offline video generation
    orch = Orchestrator()
    out = orch.create_video(
        prompt=prompt,
        total_duration=args.duration,
        output_path=args.output,
        style=args.style,
        music_path=args.music,
        interpolate_factor=args.interp
    )

    print(f"🎉 Final video saved at: {out}")

if __name__ == '__main__':
    main()
EOF

# 3. Stage & commit
git add backend/cli.py
git commit -m "feat(cli): add main CLI entrypoint"
