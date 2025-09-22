from __future__ import annotations

import ast
import contextlib
import importlib.util
import sys
import types

from importlib.machinery import SourceFileLoader
from os import PathLike
from pathlib import Path
from typing import Any

from pragma_prompt.exceptions import ConfigurationError
from pragma_prompt.exceptions import FileNotFoundError
from pragma_prompt.exceptions import LoaderError
from pragma_prompt.exceptions import ParsingError
from pragma_prompt.renderers.render_functions.block import block
from pragma_prompt.renderers.render_plan import RenderResult
from pragma_prompt.runtime_context import exec_stack_guard as rt_exec_guard
from pragma_prompt.runtime_context import render_plan_entries as rt_render_plan
from pragma_prompt.runtime_context import session as rt_session


def _derive_temp_module_name(path: Path) -> str:
    return f"pck_prompt_{abs(hash(path.resolve()))}"


def _transform_module_tree(tree: ast.Module, path: str) -> types.CodeType:
    """Rewrite module-scope string/f-string exprs into __pck_section__(content=...).

    - Matches `ast.Expr` whose value is a str constant or JoinedStr (f-string)
    - Rewrites them anywhere at module scope, including inside `if/for/while/with/try`
    - Skips inside function/class/lambda bodies
    """

    class _ModuleScopeStringToSection(ast.NodeTransformer):
        def __init__(self) -> None:
            # depth > 0 means we're inside a function/class/lambda and must not rewrite
            self._non_module_scope_depth = 0

        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:  # noqa: N802
            self._non_module_scope_depth += 1
            try:
                return self.generic_visit(node)
            finally:
                self._non_module_scope_depth -= 1

        def visit_AsyncFunctionDef(  # noqa: N802
            self, node: ast.AsyncFunctionDef
        ) -> ast.AST:
            self._non_module_scope_depth += 1
            try:
                return self.generic_visit(node)
            finally:
                self._non_module_scope_depth -= 1

        def visit_ClassDef(self, node: ast.ClassDef) -> ast.AST:  # noqa: N802
            self._non_module_scope_depth += 1
            try:
                return self.generic_visit(node)
            finally:
                self._non_module_scope_depth -= 1

        def visit_Lambda(self, node: ast.Lambda) -> ast.AST:  # noqa: N802
            # Lambdas aren't statements, but be conservative anyway.
            self._non_module_scope_depth += 1
            try:
                return self.generic_visit(node)
            finally:
                self._non_module_scope_depth -= 1

        def visit_Expr(self, node: ast.Expr) -> ast.AST:  # noqa: N802

            # Only at module scope
            if self._non_module_scope_depth == 0:
                v = node.value
                is_stringy = (
                    isinstance(v, ast.Constant) and isinstance(v.value, str)
                ) or isinstance(v, ast.JoinedStr)
                if is_stringy:
                    call = ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id="__pck_section__", ctx=ast.Load()),
                            args=[],
                            keywords=[ast.keyword(arg="content", value=v)],
                        )
                    )
                    ast.copy_location(call, node)
                    return call

            return self.generic_visit(node)

    try:
        rewriter = _ModuleScopeStringToSection()
        new_tree = rewriter.visit(tree)

        if not isinstance(new_tree, ast.AST):
            new_tree = tree

        ast.fix_missing_locations(new_tree)
        return compile(new_tree, path, "exec", dont_inherit=True)
    except SyntaxError as e:
        raise ParsingError(
            f"Syntax error while compiling transformed prompt file '{path}': {e.msg} "
            f"(line {getattr(e, 'lineno', '?')}, col {getattr(e, 'offset', '?')})"
        ) from e
    except Exception as e:
        raise ParsingError(
            f"Failed to compile transformed prompt file '{path}': {e}"
        ) from e


class _PckTopLevelStringRewriter(SourceFileLoader):
    """
    Rewrite top-level string / f-string expressions into calls:
        \"\"\"Hello\"\"\"   ->   __pck_section__(\"\"\"Hello\"\"\")
    """

    def source_to_code(  # type: ignore[override]
        self,
        data: (
            bytes
            | bytearray
            | memoryview
            | str
            | ast.Module
            | ast.Expression
            | ast.Interactive
        ),
        path: str | PathLike[str] | bytes | bytearray | memoryview,
        *,
        _optimize: int | Any = ...,
    ) -> types.CodeType:

        try:
            if isinstance(path, bytes | bytearray | memoryview):
                path_str = bytes(path).decode("utf-8", "replace")
            else:
                path_str = str(path)
        except TypeError as e:
            raise ParsingError(f"Failed to decode path: {e}") from e

        # Build AST
        try:
            if isinstance(data, ast.Module):
                tree = data
            elif isinstance(data, ast.Expression):
                tree = ast.Module(body=[ast.Expr(value=data.body)], type_ignores=[])
            elif isinstance(data, ast.Interactive):
                tree = ast.Module(body=data.body, type_ignores=[])
            else:
                try:
                    src = (
                        bytes(data).decode("utf-8")
                        if isinstance(data, bytes | bytearray | memoryview)
                        else str(data)
                    )
                except TypeError as e:
                    raise ParsingError(
                        f"Failed to decode source data for '{path_str}': {e}"
                    ) from e
                try:
                    tree = ast.parse(src, filename=path_str, mode="exec")
                except SyntaxError as e:
                    raise ParsingError(
                        f"Syntax error in prompt file '{path_str}': {e.msg} "
                        f"(line {getattr(e, 'lineno', '?')}, col {getattr(e, 'offset', '?')})"
                    ) from e
                except Exception as e:
                    raise ParsingError(
                        f"Failed to parse prompt file '{path_str}': {e}"
                    ) from e
        except ParsingError:
            raise
        except Exception as e:
            raise ParsingError(
                f"Failed to build AST for prompt file '{path_str}': {e}"
            ) from e

        # Transform
        try:
            code = _transform_module_tree(tree, path_str)
        except ParsingError:
            raise
        except Exception as e:
            raise ParsingError(
                f"Failed to transform prompt file '{path_str}': {e}"
            ) from e

        # Optional optimize flag
        if isinstance(_optimize, int):
            try:
                return compile(
                    tree, path_str, "exec", dont_inherit=True, optimize=_optimize
                )
            except SyntaxError as e:
                raise ParsingError(
                    f"Syntax error while compiling '{path_str}' with optimize={_optimize}: {e.msg} "
                    f"(line {getattr(e, 'lineno', '?')}, col {getattr(e, 'offset', '?')})"
                ) from e
            except Exception as e:
                raise ParsingError(
                    f"Failed to compile '{path_str}' with optimize={_optimize}: {e}"
                ) from e

        return code


def _exec_with_rewriter(path: Path, tmp_mod_name: str) -> None:
    """Load+exec a file using the AST rewrite, injecting __pck_section__."""
    try:
        loader = _PckTopLevelStringRewriter(tmp_mod_name, str(path))
        spec = importlib.util.spec_from_file_location(
            tmp_mod_name, str(path), loader=loader
        )
    except Exception as e:
        raise ConfigurationError(
            f"Failed creating module spec for '{path}': {e}"
        ) from e

    if spec is None or spec.loader is None:
        raise ConfigurationError(f"Cannot create import spec for {path}")

    try:
        module = importlib.util.module_from_spec(spec)
    except Exception as e:
        raise ConfigurationError(
            f"Failed to create module object for '{path}': {e}"
        ) from e

    sys.modules[tmp_mod_name] = module

    # The AST rewrite calls this
    if not callable(block):
        raise ConfigurationError("Internal renderer 'section' is not callable")
    module.__dict__["__pck_section__"] = block

    try:
        spec.loader.exec_module(module)
    except ParsingError:
        raise
    except Exception as e:
        raise LoaderError(f"Error executing prompt module '{path.name}': {e}") from e


def render_path(
    file_path: Path, *, constants: Any, context: Any, render_model: Any
) -> RenderResult:
    """
    Execute the prompt file and return the rendered text.
    Starts/ends a runtime session for this render.
    """

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    tmp_mod_name = _derive_temp_module_name(file_path)

    with (
        rt_session(constants=constants, context=context, render_model=render_model),
        rt_exec_guard(file_path),
    ):
        try:
            _exec_with_rewriter(file_path, tmp_mod_name)
            calls = rt_render_plan()
            return RenderResult(_plan=calls)
        finally:
            with contextlib.suppress(Exception):
                del sys.modules[tmp_mod_name]


def render_path_in_current_session(file_path: Path) -> None:
    """
    Execute the prompt (or component) file into the *current* active runtime session.
    Does not start/end a session. Raises RuntimeError if no session is active.
    """

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")

    # Probe for an active session; this will raise if none is active.
    _ = rt_render_plan()

    with rt_exec_guard(file_path):
        tmp_mod_name = _derive_temp_module_name(file_path)
        try:
            _exec_with_rewriter(file_path, tmp_mod_name)
        finally:
            with contextlib.suppress(Exception):
                del sys.modules[tmp_mod_name]
