# OpenAGI Lux + Kernel Browser Integration

Run [OpenAGI's Lux](https://agiopen.org) computer-use model against cloud browsers powered by [Kernel](https://onkernel.com).

## Demo

📹 **[Watch the demo video](agent_replay.mp4)** - Shows the Lux agent navigating to agiopen.org using a Kernel cloud browser.

https://github.com/user-attachments/assets/6e70fb14-9461-4f7e-ae63-f2eb92bc40b8

## What is OpenAGI?

[OpenAGI](https://agiopen.org) is an AI research organization building foundation models for computer use. Their **Lux** model is a vision-language model specifically designed to control computers by:

- Analyzing screenshots to understand the current UI state
- Deciding on the next action (click, type, scroll, etc.)
- Executing actions in a screenshot-action loop until the task is complete

## What is Kernel?

[Kernel](https://onkernel.com) provides **Browsers-as-a-Service** for AI agents and browser automation. Key features:

- **Cloud Browsers**: Instantly launch browsers without managing infrastructure
- **Computer Controls API**: Native OS-level mouse, keyboard, and screenshot controls
- **Stealth Mode**: Built-in anti-detection for reliable web automation
- **Video Replays**: Record browser sessions as MP4 videos
- **Scalability**: Run hundreds of concurrent browser sessions

## How It Works

This integration connects OpenAGI's Lux model to Kernel's cloud browsers using custom providers:

1. **`KernelScreenshotProvider`**: Captures screenshots using Kernel's Computer Controls API
2. **`KernelActionHandler`**: Translates Lux actions (click, type, scroll) to Kernel commands
3. **`KernelBrowserSession`**: Manages browser lifecycle with automatic video recording

```python
async def run_agent(instruction: str, replay_output: str = "agent_replay.mp4") -> bool:
    """Run an OpenAGI Lux agent with Kernel browser."""
    async with KernelBrowserSession(
        record_replay=True,
        replay_output_path=replay_output,
    ) as session:
        # Create the screenshot provider and action handler
        provider = KernelScreenshotProvider(session)
        handler = KernelActionHandler(session)

        # Create the OpenAGI agent
        agent = AsyncDefaultAgent(
            api_key=os.getenv("OAGI_API_KEY"),
            max_steps=20,
        )

        # Execute the task
        print(f"\nExecuting task: {instruction}\n")
        success = await agent.execute(
            instruction=instruction,
            action_handler=handler,
            image_provider=provider,
        )

        return success
```

## Setup

### 1. Install dependencies

```bash
uv pip install kernel oagi python-dotenv Pillow
```

### 2. Configure environment variables

Create a `.env` file with your API keys:

```
KERNEL_API_KEY=your_kernel_api_key
OAGI_API_KEY=your_openagi_api_key
```

Get your API keys:

- **Kernel**: [dashboard.onkernel.com](https://dashboard.onkernel.com)
- **OpenAGI**: [developer.agiopen.org](https://developer.agiopen.org)

### 3. Run the agent

```bash
python main.py
```

The agent will:

1. Launch a cloud browser via Kernel
2. Start recording a video replay
3. Execute the task using Lux's vision-action loop
4. Save the replay as `agent_replay.mp4`
5. Clean up the browser session

## Project Structure

```
├── main.py              # Entry point with example usage
├── kernel_session.py    # Browser lifecycle & replay management
├── kernel_provider.py   # Screenshot provider using Kernel API
├── kernel_handler.py    # Action handler with key translation
├── pyproject.toml       # Project dependencies
└── agent_replay.mp4     # Recorded demo video
```

## License

MIT
