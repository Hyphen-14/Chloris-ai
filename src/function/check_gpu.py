import torch

#Pengecekan sederhana
if torch.cuda.is_available():
    print("="*40)
    print("🎉🎉🎉 SUKSES! GPU DITEMUKAN! 🎉🎉🎉")
    print(f"Nama GPU kamu: {torch.cuda.get_device_name(0)}")
    print("Kita siap tancap gas training di RTX 5060!")
    print("="*40)
else:
    print("="*40)
    print("😥 YAH... GPU TIDAK DITEMUKAN. 😥")
    print("Python masih jalan di mode CPU.")
    print("Coba restart VS Code atau restart komputer.")
    print("="*40)