from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from threading import RLock

from flask import Flask, abort, redirect, render_template, request, url_for


@dataclass(slots=True)
class Todo:
    id: int
    title: str
    completed: bool = False


class TodoStore:
    def __init__(self) -> None:
        self._todos: list[Todo] = []
        self._lock = RLock()
        self._next_id = count(1)

    @staticmethod
    def _clean_title(title: str | None) -> str:
        return (title or "").strip()

    def all(self) -> list[Todo]:
        with self._lock:
            return list(self._todos)

    def add(self, title: str | None) -> Todo:
        clean_title = self._clean_title(title)
        if not clean_title:
            raise ValueError("Todo 標題不可為空")

        with self._lock:
            todo = Todo(id=next(self._next_id), title=clean_title)
            self._todos.append(todo)
            return todo

    def get(self, todo_id: int) -> Todo | None:
        with self._lock:
            return next((todo for todo in self._todos if todo.id == todo_id), None)

    def update(self, todo_id: int, title: str | None) -> Todo:
        clean_title = self._clean_title(title)
        if not clean_title:
            raise ValueError("Todo 標題不可為空")

        with self._lock:
            todo = self.get(todo_id)
            if todo is None:
                raise KeyError(todo_id)
            todo.title = clean_title
            return todo

    def toggle(self, todo_id: int) -> Todo:
        with self._lock:
            todo = self.get(todo_id)
            if todo is None:
                raise KeyError(todo_id)
            todo.completed = not todo.completed
            return todo

    def delete(self, todo_id: int) -> None:
        with self._lock:
            for index, todo in enumerate(self._todos):
                if todo.id == todo_id:
                    del self._todos[index]
                    return
            raise KeyError(todo_id)


def create_app(store: TodoStore | None = None) -> Flask:
    app = Flask(__name__)
    app.todo_store = store or TodoStore()  # type: ignore[attr-defined]

    @app.get("/")
    def home() -> object:
        return redirect(url_for("todos"))

    @app.get("/todos")
    def todos() -> str:
        editing_id = request.args.get("edit", type=int)
        return render_template(
            "index.html",
            todos=app.todo_store.all(),
            editing_id=editing_id,
        )

    @app.post("/todos")
    def add_todo() -> object:
        try:
            app.todo_store.add(request.form.get("title"))
        except ValueError as exc:
            abort(400, description=str(exc))
        return redirect(url_for("todos"))

    @app.post("/todos/<int:todo_id>/edit")
    def edit_todo(todo_id: int) -> object:
        try:
            app.todo_store.update(todo_id, request.form.get("title"))
        except KeyError:
            abort(404)
        except ValueError as exc:
            abort(400, description=str(exc))
        return redirect(url_for("todos"))

    @app.post("/todos/<int:todo_id>/toggle")
    def toggle_todo(todo_id: int) -> object:
        try:
            app.todo_store.toggle(todo_id)
        except KeyError:
            abort(404)
        return redirect(url_for("todos"))

    @app.post("/todos/<int:todo_id>/delete")
    def delete_todo(todo_id: int) -> object:
        try:
            app.todo_store.delete(todo_id)
        except KeyError:
            abort(404)
        return redirect(url_for("todos"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
