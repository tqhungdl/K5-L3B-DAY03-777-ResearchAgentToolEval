from __future__ import annotations

import argparse
from pathlib import Path

from chat_runtime import ChatSession, run_model_tool_loop  # shared with UI
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ROOT = Path(__file__).parent


def create_session(*, provider_name="openrouter", model=None, version="v3",
                   system_prompt=None, tools_path=None, transcripts_dir=None, max_tool_rounds=6):
    load_lab_env(ROOT)
    prompt_path = system_prompt or ROOT / "artifacts/system_prompt.md"
    declaration_path = tools_path or ROOT / "artifacts/tools.yaml"
    provider = make_provider(provider_name)
    return ChatSession(
        provider, system_prompt=prompt_path.read_text(encoding="utf-8"),
        tools=to_openai_tools(load_tool_declarations(declaration_path)), model=model,
        metadata={**artifact_version_dict(build_artifact_version(version, prompt_path, declaration_path)),
                  "provider": provider_name, "system_prompt": str(prompt_path), "tools": str(declaration_path)},
        transcripts_dir=transcripts_dir or ROOT / "transcripts", max_tool_rounds=max_tool_rounds,
    )


def main():
    parser = argparse.ArgumentParser(description="Research chat with exports, Telegram approval and JSON transcripts")
    parser.add_argument("--provider", required=True, choices=["openrouter", "openai", "anthropic", "gemini", "ollama", "deepseek"])
    parser.add_argument("--version", required=True)
    parser.add_argument("--model")
    parser.add_argument("--system-prompt", type=Path)
    parser.add_argument("--tools", type=Path)
    parser.add_argument("--transcripts-dir", type=Path)
    parser.add_argument("--max-tool-rounds", type=int, default=6)
    parser.add_argument("--scripted-demo", action="store_true", help="Label scripted test inputs honestly; still calls real provider/tools")
    args = parser.parse_args()
    session = create_session(provider_name=args.provider, model=args.model, version=args.version,
                             system_prompt=args.system_prompt, tools_path=args.tools,
                             transcripts_dir=args.transcripts_dir, max_tool_rounds=args.max_tool_rounds)
    session.transcript["input_mode"] = "scripted_demo" if args.scripted_demo else "interactive_cli"
    print(f"Research Agent: {session.transcript['artifact_version']}; /exit to stop")
    while True:
        try:
            user = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user in ("/exit", "/quit"):
            break
        if not user:
            continue
        record = session.turn(user)
        for event in record["tool_events"]:
            result = event["result"]
            print(f"Tool: {event['tool']} -> {result.get('status', result.get('error', 'ok'))}")
        print(f"Agent> {record['assistant_text']}")
        print(f"Transcript: {session.path}")


if __name__ == "__main__":
    main()
