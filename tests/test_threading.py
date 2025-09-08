from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from tests.includes.threading.module import ThreadingModule


def test_multithreaded_prompt_render_produces_consistent_output() -> None:
    def render_once() -> str:
        return ThreadingModule.prompt_simple.render()

    def normalize(text: str) -> str:
        # Normalize whitespace: trim ends and drop empty lines
        lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
        return "\n".join(lines)

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda _: render_once(), range(32)))

    expected = "\n".join(["threaded test", "<DATA>", "42", "</DATA>"])
    normalized_expected = normalize(expected)
    normalized_results = [normalize(r) for r in results]

    # Each thread's result matches expected content (ignoring blank lines/edges)
    assert all(r == normalized_expected for r in normalized_results)
    # All results are consistent with each other
    assert len(set(normalized_results)) == 1
