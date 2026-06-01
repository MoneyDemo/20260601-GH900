import unittest

from app import TodoStore, create_app


class TodoAppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.store = TodoStore()
        self.app = create_app(self.store)
        self.client = self.app.test_client()

    def test_home_redirects_to_todos(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].endswith("/todos"))

    def test_add_toggle_edit_and_delete_todo(self) -> None:
        response = self.client.post("/todos", data={"title": "完成報告"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("完成報告", response.get_data(as_text=True))

        todo = self.store.all()[0]
        response = self.client.post(f"/todos/{todo.id}/toggle", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.store.get(todo.id).completed)

        response = self.client.post(
            f"/todos/{todo.id}/edit",
            data={"title": "更新報告"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.store.get(todo.id).title, "更新報告")

        response = self.client.post(f"/todos/{todo.id}/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.store.get(todo.id))

    def test_blank_title_is_rejected(self) -> None:
        response = self.client.post("/todos", data={"title": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.store.all(), [])


if __name__ == "__main__":
    unittest.main()
