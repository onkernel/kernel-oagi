"""
OpenAGI Lux + Kernel Integration Example.

This script demonstrates how to run OpenAGI's Lux computer-use model
against a Kernel cloud browser using custom screenshot provider and
action handler implementations.
"""

import asyncio
import os

from dotenv import load_dotenv
from oagi.agent.tasker import TaskerAgent

from kernel_handler import KernelActionHandler
from kernel_provider import KernelScreenshotProvider
from kernel_session import KernelBrowserSession


async def run_agent(instruction: str, replay_output: str = "agent_replay.mp4") -> bool:
    """
    Run an OpenAGI Lux agent with Kernel browser.

    Args:
        instruction: The task instruction for the agent
        replay_output: Path to save the MP4 replay recording

    Returns:
        bool: True if task completed successfully
    """
    async with KernelBrowserSession(
        record_replay=True,
        replay_output_path=replay_output,
    ) as session:
        # Create the screenshot provider and action handler
        provider = KernelScreenshotProvider(session)
        handler = KernelActionHandler(session)

        # Create the OpenAGI agent
        tasker_agent = TaskerAgent(
            api_key=os.getenv("OAGI_API_KEY"),
            base_url=os.getenv("OAGI_BASE_URL", "https://api.agiopen.org"),
        )

        # Set the task
        tasker_agent.set_task(
            task="Navigate to the 'What is Computer Use' section of the OAGI homepage.",
            todos=[
            "Go to https://agiopen.org.", 
            "Make sure to press enter to start the navigation.",
            "Click on the 'What is Computer Use?' button.."
            ]
        )

        # Execute the task
        result = await tasker_agent.execute(
            instruction="",
            action_handler=handler,
            image_provider=provider
        )
        print("Execution successful: ", result)

        return result


def main():
    # Load environment variables from .env file
    load_dotenv()

    # Verify required API keys are present
    kernel_api_key = os.getenv("KERNEL_API_KEY")
    oagi_api_key = os.getenv("OAGI_API_KEY")

    if not kernel_api_key:
        raise ValueError("KERNEL_API_KEY not found in .env file")
    if not oagi_api_key:
        raise ValueError("OAGI_API_KEY not found in .env file")

    # Example task
    instruction = (
        "Go to https://agiopen.org. Make sure to press enter to start the navigation."
    )
    replay_path = "agent_replay.mp4"

    # Run the agent
    success = asyncio.run(run_agent(instruction, replay_output=replay_path))

    if success:
        print("\n✓ Task completed successfully!")
        print(f"📹 Replay saved to: {replay_path}")
    else:
        print("\n✗ Task did not complete within max steps")
        print(f"📹 Replay saved to: {replay_path}")


if __name__ == "__main__":
    main()
