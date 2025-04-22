# 🖼️ NVIDIA AI Visual Tools - Text ↔ Image with Gradio

這是一個使用 NVIDIA API 串接的雙向影像生成與辨識應用：
- **Text-to-Image**：輸入文字提示，由 NVIDIA Nim API 產生圖片。
- **Image-to-Text**：上傳圖片，透過 NVIDIA Integrate API 回傳繁體中文描述。

---

## 📂 專案結構

```bash
.
├── text_to_image.py        # 使用文字生成圖片
├── image_to_text.py        # 上傳圖片並轉為繁體中文描述
├── .env                    # 儲存 API 金鑰（不應上傳至 GitHub）
├── README.md               # 本說明文件
```

---

## 🚀 使用方式

### 1. 安裝相當套件
```bash
pip install -r requirements.txt
```

**requirements.txt** 推薦內容:
```txt
gradio
requests
python-dotenv
Pillow
```

### 2. 設定 `.env` 檔案

新增 `.env` 檔，填入 API 金鑰：

```env
# Text-to-Image
NVIDIA_NIM_API_KEY=your-text-to-image-api-key
NVIDIA_NIM_API_URL=https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev

# Image-to-Text
NV_IMAGE2TEXT_API_KEY=your-image-to-text-api-key
NV_IMAGE2TEXT_API_URL=https://integrate.api.nvidia.com/v1/chat/completions
```

> ✅ **請加入 `.env` 至 `.gitignore`，避免金鑰外洩**

---

### 3. 執行模組

#### 文字 → 圖片
```bash
python text_to_image.py
```
開啟 Gradio 之後，輸入例如：
> a cozy cafe interior

#### 圖片 → 文字
```bash
python image_to_text.py
```
上傳一張圖片，將會返回簡潔的繁體中文描述。

---

## 🌐 範例畫面

| 模型 | 範例 |
|--------|--------|
| Text → Image | `a magical forest in winter` ![](demo-cafe.jpg) |
| Image → Text | 上傳小狗照片 → `這是一隻黃色小狗坐在草地上` |

---

## 📌 注意事項
- 因 NVIDIA API 限制，圖片最大繼續碼長度為 **180KB**
- 大圖會自動壓縮與縮小
- 輸出默認為 **繁體中文**

---

## 🤖 自訂

若你需要:
- `requirements.txt`
- `.gitignore`
- 圖片 demo / icon

可以說一聲，我會更新為你配套🚀

---

## 🧠 致謝

本項目使用:
- NVIDIA AI API (Nim & Integrate)
- [Gradio](https://gradio.app)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

