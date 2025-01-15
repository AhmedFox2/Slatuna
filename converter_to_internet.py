import os
import json
import base64

def split_file_to_json(file_path, chunk_size):
    file_size = os.path.getsize(file_path)
    chunks = []

    with open(file_path, 'rb') as file:
        chunk = file.read(chunk_size)
        chunk_number = 0

        while chunk:
            encoded_chunk = base64.b64encode(chunk).decode('utf-8')  # ترميز chunk إلى base64 وتخزينه كـ نص
            chunks.append({
                "chunk_number": chunk_number,
                "chunk_data": encoded_chunk
            })
            chunk_number += 1
            chunk = file.read(chunk_size)

    json_data = {"chunks": chunks}
    json_file_path = f"{file_path}.json"
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file)

    return json_file_path

def reconstruct_file_from_json(json_file_path, output_file_path):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    chunks = json_data['chunks']
    with open(output_file_path, 'wb') as output_file:
        for chunk in chunks:
            chunk_data = base64.b64decode(chunk['chunk_data'])  # فك ترميز chunk من base64 إلى bytes
            output_file.write(chunk_data)
    print(f"تم إعادة بناء الملف: {output_file_path}")

if __name__ == "__main__":
    json_file_path = 'rufus-4.6.exe.json'
    output_file_path = 'rufus-4.6.exe'
    reconstruct_file_from_json(json_file_path, output_file_path)