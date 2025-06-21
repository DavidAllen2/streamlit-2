import os
import subprocess
import streamlit as st
import threading
import asyncio

# 设置页面
st.set_page_config(page_title="Honey-Girl", layout="wide")

# UI 控制状态
if "running" not in st.session_state:
    st.session_state.running = False
    st.session_state.logs = ""
    st.session_state.sub = ""
    st.session_state.argo = ""

st.title("🌐 Honey-Girl")

# 环境变量
envs = {
    "BOT_TOKEN": st.secrets.get("BOT_TOKEN", ""),
    "CHAT_ID": st.secrets.get("CHAT_ID", ""),
    "ARGO_AUTH": st.secrets.get("ARGO_AUTH", ""),
    "ARGO_DOMAIN": st.secrets.get("ARGO_DOMAIN", ""),
    "NEZHA_KEY": st.secrets.get("NEZHA_KEY", ""),
    "NEZHA_PORT": st.secrets.get("NEZHA_PORT", ""),
    "NEZHA_SERVER": st.secrets.get("NEZHA_SERVER", ""),
}

# 写出 .env 文件
with open("./env.sh", "w") as shell_file:
    shell_file.write("#!/bin/bash\n")
    for k, v in envs.items():
        os.environ[k] = v
        shell_file.write(f"export {k}='{v}'\n")

# 后台启动函数（安装依赖 + 启动 app.py）
def run_backend():
    try:
        subprocess.run("chmod +x app.py", shell=True, check=True)
        subprocess.run("pip install -r requirements.txt", shell=True, check=True)
        subprocess.Popen(["python", "app.py"])
        st.session_state.running = False
        st.session_state.logs += "\n✅ 已自动部署完成"
    except Exception as e:
        st.session_state.logs += f"\n❌ 出错: {e}"
        st.session_state.running = False

# 定义异步主函数
async def main():
    st.session_state.running = True
    run_backend()

# ✅ 自动启动机制：首次加载时执行部署（用 flag 避免重复）
if not os.path.exists("/tmp/deployed.flag"):
    def auto_start():
        asyncio.run(main())
        with open("/tmp/deployed.flag", "w") as f:
            f.write("done")
    threading.Thread(target=auto_start, daemon=True).start()
    st.info("正在自动部署，请稍候...")

# 🖱️ 手动按钮也保留（可用于用户主动重新触发）
if st.button("🚀 启动部署"):
    if not st.session_state.running:
        threading.Thread(target=lambda: asyncio.run(main()), daemon=True).start()
        st.success("✅ 已开始执行部署任务")
    else:
        st.warning("⚠️ 部署任务已在运行中")

# 展示视频
video_paths = ["./meinv.mp4", "./mv2.mp4"]
for path in video_paths:
    if os.path.exists(path):
        st.video(path)

# 展示图片
image_path = "./mv.jpg"
if os.path.exists(image_path):
    st.image(image_path, caption="南音", use_container_width=True)