import torch

print("Torch:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))
print("Capability:", torch.cuda.get_device_capability(0))

# Tes bikin tensor di GPU
x = torch.randn(5000, 5000).cuda()
y = torch.randn(5000, 5000).cuda()
z = torch.matmul(x, y)

print("Matrix multiply success!")
