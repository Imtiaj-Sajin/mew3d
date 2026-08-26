"""PromptSmith agent: turns the user's text into a 3D-reconstruction-friendly image prompt."""

from .base import Agent

PROMPT_SYSTEM = """You are a prompt engineer for a text-to-image model whose output feeds a
single-image 3D reconstruction model (TripoSR). The image MUST show the ENTIRE object -
nothing cut off by any frame edge, with clear empty margin around it on all sides. Also:
one single object, centered, 3/4 view, plain uncluttered background, even studio lighting,
no text or watermarks. NEVER a close-up or macro shot. Start the prompt with phrasing like
"full view of a whole <object>". Reply with JSON:
{"prompt": "<the enhanced prompt, under 60 words>",
 "negative_prompt": "<things to avoid - always include close-up, macro, cropped>",
 "reasoning": "<one sentence on your choices>"}"""

FALLBACK_SUFFIX = (
    ", full view of the whole object, entire object visible with margin around it, "
    "single object, centered composition, 3/4 view, plain light gray background, "
    "soft studio lighting, highly detailed, product photography style"
)
FALLBACK_NEGATIVE = (
    "close-up, macro, cropped, partial view, zoomed in, out of frame, multiple objects, "
    "text, watermark, busy background, harsh shadows, blurry, low quality, human hands"
)


class PromptSmithAgent(Agent):
    name = "PromptSmith"
    icon = "✍️"
    description = "enhances the text prompt for image generation"

    def execute(self):
        user_text = self.cfg.text
        subject = self.ctx.state.get("analysis", {}).get("subject", user_text)
        advice = self.ctx.state.get("analysis", {}).get("advice", "")

        result = self.llm.chat_json(
            self.name, PROMPT_SYSTEM,
            f"User request: {user_text!r}. Subject: {subject!r}. "
            + (f"Analyst advice: {advice}" if advice else ""),
        )
        if result and result.get("prompt"):
            prompt = result["prompt"]
            negative = result.get("negative_prompt", FALLBACK_NEGATIVE)
            self.decision(f"LLM-enhanced prompt: {prompt!r}",
                          reasoning=result.get("reasoning", ""))
        else:
            prompt = user_text + FALLBACK_SUFFIX
            negative = FALLBACK_NEGATIVE
            self.decision(f"heuristic-enhanced prompt: {prompt!r} (LLM unavailable)")

        enhanced = {"original": user_text, "prompt": prompt, "negative_prompt": negative}
        self.ctx.state["enhanced_prompt"] = enhanced
        self.ctx.save_json("logs/prompt.json", enhanced)
        return enhanced
