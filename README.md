# Todo Demo（Python / Flask）

這是一個以 **Python + Flask** 實作的簡易 Todo Demo 網站，資料只會暫存在記憶體中，重啟服務後就會清空。

## 功能

- 新增 Todo
- 檢視 Todo 清單
- 編輯 Todo
- 刪除 Todo
- 切換完成 / 未完成

## 專案結構

```
project/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```

## 快速啟動

### 1. 安裝套件

```bash
pip install -r requirements.txt
```

### 2. 啟動服務

```bash
python app.py
```

### 3. 開啟瀏覽器

前往：

```text
http://127.0.0.1:5000/todos
```

## API 路由

- `GET /todos`：取得 Todo 頁面
- `POST /todos`：新增 Todo
- `POST /todos/<id>/edit`：編輯 Todo
- `POST /todos/<id>/delete`：刪除 Todo
- `POST /todos/<id>/toggle`：切換完成狀態

## 測試

```bash
python -m unittest discover -s tests -v
```
