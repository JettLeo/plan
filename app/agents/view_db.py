# view_db.py
import sqlite3
import json
import pickle
import base64

def view_checkpoints(db_path="checkpoints.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. 查看所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📋 数据库中的表:", [t[0] for t in tables])
    print("-" * 50)

    # 2. 查看 checkpoints 表结构
    cursor.execute("PRAGMA table_info(checkpoints);")
    columns = cursor.fetchall()
    print("📋 checkpoints 表的字段:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    print("-" * 50)

    # 3. 查看 checkpoints 表的原始数据（前5条）
    cursor.execute("SELECT thread_id, checkpoint_id, checkpoint FROM checkpoints LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        thread_id, checkpoint_id, blob = row
        print(f"🔹 thread_id: {thread_id}, checkpoint_id: {checkpoint_id}")
        # 打印 blob 的前 100 个字节的十六进制表示
        hex_preview = blob[:50].hex() if blob else "empty"
        print(f"   blob 前50字节(hex): {hex_preview}")
        # 尝试用 UTF-8 解码看是否是人类可读
        try:
            text = blob[:200].decode('utf-8', errors='ignore')
            print(f"   blob 前200字符: {text}")
        except:
            pass
        print("-" * 30)

    # 4. 查看 writes 表的原始数据（前5条）
    cursor.execute("SELECT thread_id, checkpoint_id, task_id, value FROM writes LIMIT 5;")
    rows = cursor.fetchall()
    if rows:
        print("📋 writes 表前5条原始记录:")
        for row in rows:
            thread_id, checkpoint_id, task_id, blob = row
            print(f"🔹 thread_id: {thread_id}, checkpoint_id: {checkpoint_id}, task_id: {task_id}")
            try:
                # 尝试用 pickle 反序列化
                value = pickle.loads(blob)
                print(f"   value (pickle): {value}")
            except:
                try:
                    # 尝试用 JSON 反序列化
                    value = json.loads(blob.decode('utf-8'))
                    print(f"   value (json): {value}")
                except:
                    print(f"   blob 前50字节(hex): {blob[:50].hex()}")
            print("-" * 30)

    conn.close()

if __name__ == "__main__":
    view_checkpoints()