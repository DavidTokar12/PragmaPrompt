"""Template helpers for prompt composition."""

from __future__ import annotations


def few_shot(question: str, answer: str) -> str:
    """Format a question-answer pair for few-shot prompting.

    Args:
        question: The input question
        answer: The expected answer

    Returns:
        Formatted few-shot example
    """
    return f"Question: {question}\nAnswer: {answer}"


def chain_of_thought(question: str, thought: str, answer: str) -> str:
    """Format a chain-of-thought example with reasoning.

    Args:
        question: The input question
        thought: The reasoning process
        answer: The final answer

    Returns:
        Formatted chain-of-thought example
    """
    return f"Question: {question}\nThought: {thought}\nAnswer: {answer}"


def react_step(thought: str, action: str, observation: str) -> str:
    """Format a single ReAct (Reason-Act) step.

    Args:
        thought: The reasoning behind the action
        action: The action to take
        observation: The result of the action

    Returns:
        Formatted ReAct step
    """
    return f"Thought: {thought}\nAction: {action}\nObservation: {observation}"
