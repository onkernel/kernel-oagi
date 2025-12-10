# OpenAGI Lux + Kernel Browser Integration

Run [OpenAGI's Lux](https://agiopen.org) computer-use models against serverless browsers powered by [Kernel](https://onkernel.com).

## Demo

📹 **[Watch the demo video](https://github.com/user-attachments/assets/6e70fb14-9461-4f7e-ae63-f2eb92bc40b8)** - Shows the Lux agent navigating to agiopen.org using a Kernel serverless browser.


## What is OpenAGI?

[OpenAGI](https://agiopen.org) is an AI research organization building foundation models for computer use. Their **Lux** model is a vision-language model specifically designed to control computers by:

- Analyzing screenshots to understand the current UI state
- Deciding on the next action (click, type, scroll, etc.)
- Executing actions in a screenshot-action loop until the task is complete

## What is Kernel?

[Kernel](https://onkernel.com) provides **Browsers-as-a-Service** for AI agents and browser automation. Key features:

- **Serverless Browsers**: Instantly launch browsers without managing infrastructure
- **Computer Controls API**: Native OS-level mouse, keyboard, and screenshot controls
- **Stealth Mode**: Built-in anti-detection for reliable web automation
- **Video Replays**: Record browser sessions as MP4 videos
- **Scalability**: Run hundreds of concurrent browser sessions

## Model Selection

Choose the right model for your task:

| Model | Best For | Avoid When |
|-------|----------|------------|
| `lux-actor-1` | Fast execution (1s/step), simple linear tasks (10-20 steps) | Complex reasoning, comparison, or handling ambiguous instructions |
| `lux-thinker-1` | Complex planning, comparison tasks ("find cheapest"), handling ambiguity | Low latency needs or simple click-paths |

## Usage Approaches

| Approach | Best For | Trade-offs |
|----------|----------|------------|
| **AsyncDefaultAgent** (Actor) | Fast UI control, short tasks, real-time automation | Requires clear, step-by-step instructions |
| **AsyncDefaultAgent** (Thinker) | Research tasks, ambiguous goals, complex planning | Slower execution, best for async workflows |
| **TaskerAgent** (Actor) | Multi-step forms, structured workflows, repeatable processes | Requires defining todos upfront |

## How It Works

This integration connects OpenAGI's Lux model to Kernel's serverless browsers using custom providers:

1. **`KernelScreenshotProvider`**: Captures screenshots using Kernel's Computer Controls API
2. **`KernelActionHandler`**: Translates Lux actions (click, type, scroll) to Kernel commands
3. **`KernelBrowserSession`**: Manages browser lifecycle with automatic video recording

### AsyncDefaultAgent Example

Use `AsyncDefaultAgent` for high-level, tasks with either the `lux-actor-1` model for immediate tasks or `lux-thinker-1` for more complex, longer running tasks:

```python
async with KernelBrowserSession(
    record_replay=True,
    replay_output_path=replay_output,
) as session:
    # Create the screenshot provider and action handler
    provider = KernelScreenshotProvider(session)
    handler = KernelActionHandler(session)

    agent = AsyncDefaultAgent(
        api_key=os.getenv("OAGI_API_KEY"),
        max_steps=20,
        model="lux-actor-1"  # or "lux-thinker-1" for complex planning tasks
    )

    # Execute the task
    print(f"\nExecuting task: {instruction}\n")
    success = await agent.execute(
        instruction=instruction,
        action_handler=handler,
        image_provider=provider,
    )
```

### TaskerAgent Example

Use `TaskerAgent` for structured workflows with predefined steps:

```python
async with KernelBrowserSession(
    record_replay=True,
    replay_output_path=replay_output,
) as session:
    provider = KernelScreenshotProvider(session)
    handler = KernelActionHandler(session)

    tasker_agent = TaskerAgent(
        api_key=os.getenv("OAGI_API_KEY"),
        base_url=os.getenv("OAGI_BASE_URL", "https://api.agiopen.org"),
    )

    tasker_agent.set_task(
        task="Navigate to the 'What is Computer Use' section of the OAGI homepage.",
        todos=[
            "Go to https://agiopen.org.",
            "Make sure to press enter to start the navigation.",
            "Click on the 'What is Computer Use?' button."
        ]
    )

    result = await tasker_agent.execute(
        instruction="",
        action_handler=handler,
        image_provider=provider
    )
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

For `AsyncDefaultAgent` (supports `lux-actor-1` or `lux-thinker-1`):

```bash
python agent_default.py
```

For `TaskerAgent` (structured workflows with todos):

```bash
python agent_tasker.py
```

The agent will:

1. Launch a serverless browser via Kernel
2. Start recording a video replay
3. Execute the task using Lux's vision-action loop
4. Save the replay as `video_agent_replay.mp4`
5. Clean up the browser session

## Project Structure

```
├── agent_default.py       # AsyncDefaultAgent example (lux-actor-1/lux-thinker-1)
├── agent_tasker.py        # TaskerAgent example with todos (lux-actor-1)
├── kernel_session.py      # Browser lifecycle & replay management
├── kernel_provider.py     # Screenshot provider using Kernel API
├── kernel_handler.py      # Action handler with key translation
├── pyproject.toml         # Project dependencies
└── video_agent_replay.mp4       # Recorded demo video
```

## License

MIT
